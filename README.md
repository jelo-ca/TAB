# TAB Discord Bot

A Discord bot designed for musicians to track their practice progress, share recordings, and discover guitar tabs.

## Features

### Level System
- Gain XP by posting audio/video practice recordings
- Earn bonus XP from community reactions
- Track daily practice streaks
- Level up and view progress with detailed stats

### Music Sheet System
- Search for guitar tabs on Songsterr
- Favorite and save your favorite songs
- Quick access to your saved music sheets

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv .
   ```
3. Activate the virtual environment:
   - Windows: `Scripts\activate.bat`
   - Linux/Mac: `source Scripts/activate`
4. Install dependencies:
   ```bash
   pip install discord.py beautifulsoup4 requests python-dotenv
   ```

## Setup

1. Create a `.env` file in the root directory
2. Add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
3. Run the bot:
   ```bash
   python src/main.py
   ```

## Commands

### Level System
- `&register` - Register for the leveling system
- `&stats` - View your current level, XP, and streak
- `&practice` - Send a daily practice request for peer approval
- `&notice @user` - Approve someone's practice and give them XP

### Music Sheets
- `&search <song name>` - Search for guitar tabs on Songsterr
- `&favorite <songsterr_url>` - Add a song to your favorites
- `&favorites` - View your favorited songs

## Requirements

- Python 3.8+
- discord.py
- beautifulsoup4
- requests
- python-dotenv

## How It Works

### Practice Tracking
Users can post audio/video files of their practice sessions to gain XP. Community members can react to these posts to give additional XP to both the poster and reactor.

### Daily Practice
Users can send daily practice requests that require peer approval. Maintaining streaks gives bonus XP when approving others.

### Music Discovery
Search for guitar tabs directly in Discord and save your favorites for easy access later.

## Contributing

Feel free to submit issues and pull requests!</content>
<parameter name="filePath">c:\Users\anjoe\OneDrive\Desktop\Projects\TAB\README.md