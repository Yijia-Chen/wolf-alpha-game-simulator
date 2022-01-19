# Wolf Alpha Game Simulation

Wolf Game is a fascinating NFT-based strategy game based highly on game theory and real-time decision making. As the [Alpha Game](https://wolf.game/alpha-game-whitepaper) is launching on Jan 19, 2022, I wished to develop a simulator which predicts things that may happen as the game unfolds and players adopt different strategies. So here it is. I hope that the framework set up can help people with all kinds of strategies how they play out with respect to other players.

**This repo is a work in progress.**

## How to Use

The `utility` folder contains all constants, variables, and components of the game. The `strategy` folder contains two types of strategies, leader (pack) or non-alpha player, both of which can have specific implementations regarding rank, expected return, and risk tolerance.

To simulate, first edit `variables.py` in `utility` as it contains quantities non-measureable before the game starts. Then update both your desired strategies and suspected strategies for other players. Once you finalize strategies, use `simulation.py` to simulate in a Simpy environment using constants and variables in `utility`. Have fun!

If you wish to contribute, kindly open an issue, or reach me [here](https://twitter.com/0x1plus).

## Disclaimers

- If the project completion is on a scale of 1 to 10, currently this repo is perhaps at 3 or 4 at best - still at inception. Some interesting things yet to be done/being worked on include:
  - Simpy simulation of game and use of env instead of real time
  - More nuanced strategies
  - Usage of more variables such as $WOOL token price
  - **_Multiplayer cooperation/collusion, possibly contract-based_**
  - **_Portfolio management for single player owning multiple animals_**
- No part of the project is meant for financial advice.
