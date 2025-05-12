# super-funicular

# TFN CTV Project

## File Upload Functionality

This project now supports file uploads for various media types:

### Supported Upload Types
- **Artist Images**: Upload images for artists
- **Album Cover Images**: Upload cover images for albums
- **Track Audio Files**: Upload audio files for tracks
- **Ad Campaign Videos**: Upload videos for ad campaigns

### Where Uploads Go
All uploaded files are stored in the `media/` directory at the project root, organized in subdirectories:
- Artist images: `media/artists/`
- Album cover images: `media/albums/`
- Track audio files: `media/tracks/`
- Ad campaign videos: `media/ads/`

Files are automatically renamed using UUID to prevent filename conflicts.

### Testing File Uploads
To test file uploads:
1. Navigate to the appropriate form (e.g., ad campaign upload form)
2. Select a file to upload
3. Submit the form
4. The file will be uploaded to the appropriate directory

### Placeholder Images
The project uses placeholder SVG graphics from the static directory when no images are available.

If you want to use the Pexels API for placeholder images:
1. Get a Pexels API key from [Pexels API](https://www.pexels.com/api/)
2. Add your API key to the `.env` file:
   ```
   PEXELS_API_KEY=your_pexels_api_key_here
   ```
3. If you don't have python-dotenv installed, you can install it with:
   ```
   pip install python-dotenv
   ```
   Then uncomment the dotenv loading code in `tfn_ctv/settings.py`

### Dependencies
- Django 5.2.1
- For image processing (optional): Pillow
  ```
  pip install Pillow
  ```
