# YouTube Shorts Automation
The goal of this project is to fully automate the process of creating YouTube short content videos, from the basic idea of the video all the way through the uploading of the videos to YouTube.

This project serves as a crude example of utilizing API tokens, and though simple, this does indeed function given the proper API keys and sufficient OpenAI tokens. 

## Usage
- To use this project, you will simply need to:
- modify the script file to fit your needs
and 
- add the music and template mp4 files to the project.

<----------------------------------------------------------------------------------------------------------------------->
First, modify line 13, the API key, in the script file:
<pre>
openai.api_key = '#REDACTED'
</pre>
Replace REDACTED with the proper API key.
Next, modify line 37, idea prompt:
<pre>
        video_idea_prompt = "Generate an inspirational quote for a YouTube short targeting the age group 12-20 in the format of: [##insert quote here] Do not elaborate or explain the quote at all, I only want the quote"
</pre>
You will want to replace this prompt with whatever you wish to place onto the short. This can be changed a lot, and really should be more specific than it currently is. Adding character limits could further narrow down the quote so that FFMPEG can ensure proper formatting.

Finally, add music files and template files that you will be using for the shorts. You can add as many as you wish, they simple must be specified in line 51, 
<pre>
 video_files = ['#REDACTED']
 </pre>
 and line 67,
 <pre>
         music_files = ['#REDACTED']
</pre>

