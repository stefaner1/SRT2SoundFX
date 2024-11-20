import os, concurrent
import subprocess
import tempfile

class AudioPlacer:
        
    def get_audio_duration(self, audio_path):
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', audio_path], text=True, capture_output=True)
        return float(result.stdout.strip())
    def process_audio_chunk(self, sentences_chunk, temp_dir, chunk_idx, next_chunk_start_time):
        # Create the initial part of the ffmpeg command
        ffmpeg_cmd = ['ffmpeg', '-y']

        # Add inputs and filters for each sentence in the chunk
        filter_complex_parts = []
        current_time = sentences_chunk[0]['start'] if chunk_idx > 0 else 0
        i = 0  # Input index
        for sentence in sentences_chunk:
            if "audio_path" not in sentence or sentence["audio_path"] is None:              
                 continue

            
            silence_duration = sentence['start'] - current_time
            if silence_duration < 0:
                sentence['start']=current_time
                print(f"The last audio was too long, so there is no pause between sentences. Current sentence: {str(sentence)}")     
                # raise Exception("Error processing audio chunk", f"The sentence audio is broken. Wrong silence_duration: {silence_duration}, sentence {str(sentence)}")
            if silence_duration > 0:
                # Add silence audio
                ffmpeg_cmd.extend(['-f', 'lavfi', '-t', str(silence_duration), '-i', 'anullsrc=r=44100:cl=mono'])
                filter_complex_parts.append(f"[{i}:a]")
                i += 1

            audio_file_path = os.path.join(sentence['audio_path'])
            audio_duration = self.get_audio_duration(audio_file_path)
            fade_duration= (1 if audio_duration>5 else 0.5) if audio_duration>2 else 0.2
            audio_faded_file_path = self.apply_afade(audio_file_path, audio_duration, fade_duration)
            ffmpeg_cmd.extend(['-i', audio_faded_file_path])
            filter_complex_parts.append(f"[{i}:a]")
            i += 1
                
            current_time = sentence['start']+audio_duration

        # Append silence at the end of the chunk if needed
        if next_chunk_start_time is not None:
            silence_duration = round(next_chunk_start_time - current_time, 2)
            if silence_duration > 0:
                ffmpeg_cmd.extend(['-f', 'lavfi', '-t', str(silence_duration), '-i', 'anullsrc=r=44100:cl=mono'])
                filter_complex_parts.append(f"[{i}:a]")

        # Build the filter_complex string
        filter_complex = ''.join(filter_complex_parts) + f"concat=n={len(filter_complex_parts)}:v=0:a=1[aout]"

        # Output file for the chunk
        chunk_audio_path = os.path.join(temp_dir, f'chunk_{chunk_idx}.mp3')
        ffmpeg_cmd += ['-filter_complex', filter_complex, '-map', '[aout]', '-q:a', '0', chunk_audio_path]

        # Run the ffmpeg command
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            raise Exception("Error processing audio chunk", error_message)

        return chunk_audio_path
    
    def apply_afade(self, audio_path, audio_duration, fade_duration=0.5):
        new_audio_path= audio_path.replace(".mp3", "_faded.mp3")
        ffmpeg_cmd= ['ffmpeg', '-y', '-i', audio_path, '-af', f'afade=t=in:st=0:d={fade_duration},afade=t=out:st={audio_duration-fade_duration}:d={fade_duration}', '-q:a', '0', new_audio_path]
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            raise Exception("Error applying fade effect", error_message)
        return new_audio_path
        
    def merge_effects(self, sentences, temp_dir, final_audio_name):
        
        CHUNK_SIZE = 100  # Define your chunk size
        chunk_size=0
        sentences_chunk=[]
        chunk=[]
        next_chunk_start_time=0

        for idx, sentence in enumerate(sentences):            
            chunk.append(sentence)
            chunk_size += 1

            if chunk_size >= CHUNK_SIZE:
                if idx != (len(sentences)-1):
                    next_chunk_start_time = sentences[idx+1]['start']
                sentences_chunk.append({"chunk":chunk.copy(), "next_chunk_start_time":next_chunk_start_time})
                chunk = []
                chunk_size = 0

        if chunk:
            sentences_chunk.append({"chunk":chunk})

        # Process chunks in parallel
        merged_paths= [None] * len(sentences_chunk)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(self.process_audio_chunk, chunk["chunk"], temp_dir, i, chunk.get("next_chunk_start_time")): i for i, chunk in enumerate(sentences_chunk)}
            for future in concurrent.futures.as_completed(futures):
                index = futures[future]
                result = future.result()
                merged_paths[index] = result  # Place the result in the correct position
                
            

        # Combine all chunk audios
        combined_audio_path = os.path.join(temp_dir, final_audio_name)
        ffmpeg_merge_cmd = ['ffmpeg', '-y', '-i', 'concat:' + '|'.join(merged_paths), '-q:a', '0', combined_audio_path]
        
        result = subprocess.run(ffmpeg_merge_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            raise Exception("Error merging audios ", error_message)

        for path in merged_paths:
            os.remove(path)

        return combined_audio_path

    def sounds_to_audiobook(self, audiobook_path, combined_audio_path, temp_dir, final_audiobook_name='final_audiobook_with_effects.mp3', volume_adjustment=-10):
        """Adds the combined MP3 to audiobook file."""
        final_audiobook_path = os.path.join(temp_dir, final_audiobook_name)
        ffmpeg_cmd = [
            'ffmpeg', '-y', 
            '-i', audiobook_path, 
            '-i', combined_audio_path, 
            '-filter_complex', f'[1:a]volume={volume_adjustment}dB[volume_adjusted]; [0:a][volume_adjusted]amix=inputs=2[aout]', 
            '-map', '[aout]', 
            '-q:a', '0',  # highest quality
            final_audiobook_path
        ]

        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            raise Exception("Error merging audios", error_message)

        return final_audiobook_path

    def add_sounds_to_audio(self, audiobook_path, sentences, temp_dir, final_audiobook_name="final_audiobook_with_effects.mp3", final_effects_name="effects.mp3", volume_adjustment=-10):

        # Combine the effects audio files
        combined_audio_path = self.merge_effects(sentences, temp_dir, final_effects_name)

        # Add the combined effects to the audio
        final_audiobook_path = self.sounds_to_audiobook(audiobook_path, combined_audio_path, temp_dir, final_audiobook_name, volume_adjustment)

        return {"effects": combined_audio_path, "final_audio": final_audiobook_path}
