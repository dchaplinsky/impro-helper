impro-helper
============

A web-service for jazz scores analysis heavily inspired by Coursera's “Introduction to improvisation” course taught by Gary Burton.

# In a nutshell
Impro helper is a Flask based web service which allows to upload MusicXML files with harmony and melodic line 
of some jazz tune and analyses it determining notes used in the harmony and melody. This information is then being used to 
suggest modes/scales to use over each chord when improvising. 

## TODO
* Complete the analysis with actual suggestions of modes (and generate proper explanation for each choice).
* Analyse harmony for common scales, melodic lines, pedals and things.
* Add some design for a web version.
* Add some options for tie breaking and actual meaning of chord names.
* Support for other dialects of MusicXML.

## Requirements for CLI version
* mingus
* lxml

## Additional requirements for web version
* Flask

## Live demo
Project is actually deployed on heroku: http://impro-helper.herokuapp.com/

## How to try it
Repo has two XML files (“500 Miles High” by Chick Corea and “Memories of Tomorrow” by Keith Jarrett) 
exported from MuseScore. You can use them with CLI version or web version (see the link above)

## Footnotes
It's still pretty much work in progress but I decided to share it to motivated myself to complete it. 
And it still might be useful even in current state.
