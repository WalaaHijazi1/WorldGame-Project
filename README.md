# 𝕎𝕠𝕣𝕝𝕕 𝕆𝕗 𝔾𝕒𝕞𝕖𝕤 ℙ𝕣𝕠𝕛𝕖𝕔𝕥
#     𝕎𝕒𝕝𝕒𝕒 ℍ𝕚𝕛𝕒𝕫𝕚


In this project I built three Games:
### CurrencyRoulette Game:
This game challenges the user to guess the value in ILS (Israeli Shekel) of a randomly generated amount in USD. The current exchange rate is fetched live using a currency API. Based on the difficulty level, a tolerance interval is calculated around the correct ILS value, and the user wins if their guess falls within that range.


### Guess Game:
In this simple number guessing game, the system generates a random number between 1 and the chosen difficulty level. The player must guess the exact number to win. The game ensures input validation and provides appropriate feedback.

### Memory Game:
This game tests the user's short-term memory by displaying a sequence of random numbers for a brief period (default 10 seconds). The user must recall and enter the exact sequence in the correct order. Winning depends on accurate memory recall.





<p align="center">
  <img src="images/FlowChart_worldGame.png" alt="Jenkins Flow Chart" width="500" height="700">
</p>

Jenkins File Explenation:
The pipeline runs on any available node.
Before the pipeline I defined an Option block that configures how the pipeline behaves:
the block automatically delets old builds and states to delete builds after 5 days, and no more than 20 builds should be saved.
the trigger block define when the pipeline should start a build, for example in this specific pipeline it starts building every 30 minutes (every hour).
the 'environment' block defines an environment variable that is used through the pipeline.