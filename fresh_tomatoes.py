import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Yshia's Favourite Movies Website</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .container-movie .row {
            display: flex;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding: 30px;
        }
        .movie-tile:hover {
            background-color: #eee;
            cursor: pointer;
        }
        .poster-container {
            position: relative;
            overflow: hidden;
            width: 220px;
            height: 342px;
            margin: 0 auto;
        }
        .poster-overlay {
            position: absolute;
            top: 342px;
            height: 100%;
            padding: 20px;
            color: #ddd;
            transition: 0.5s;
            background: rgba(0, 0, 0, 0.75);
        }
        .poster-overlay.active {
            top: 0;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        $(document).ready(function () {
            // Animate in the movies when the page loads
            $('.movie-tile').hide().first().show(500, function showNext() {
                // Wrap every 3 movie-tile divs in a div with class 'row'
                var tiles = $('.container-movie > .movie-tile');
                for(var i = 0; i < tiles.length; i+=3) {
                    $('.movie-tile').next("div").show(500, showNext); // animate tiles
                    tiles.slice(i, i+3).wrapAll("<div class='row'></div>"); // wrap 3 tiles in a row
                }
            });
            $('.poster-container').hover(function(){
                $(this).find('.poster-overlay').toggleClass('active');
            })
        });
    </script>
</head>
'''


# The main page layout and title bar
main_page_content = '''
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Yshia'a Favourite Movies</a>
          </div>
          <div class="collapse navbar-collapse">
            <p class="navbar-text navbar-right">Watch trailers, read my random commentary.</p>
          </div>
        </div>
      </div>
    </div>
    <div class="container container-movie">
      {movie_tiles}
    </div>
  </body>
</html>
'''


# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <div class="poster-container">
        <div class="poster-overlay text-left">
        <h4>{movie_title}</h4>
        <p>{movie_storyline}</p>
        </div>
        <img class="poster-image" src="{poster_image_url}" width="220" height="342">
    </div>
    <h3>{movie_title} <span class="lead">({movie_year})</span></h3>
    <hr>
    <h5 class="text-left">Thoughts</h5>
    <p class="text-left">{movie_thoughts}</p>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(
            r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(
            r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = (youtube_id_match.group(0) if youtube_id_match
                              else None)

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            movie_year=movie.year,
            movie_storyline=movie.storyline,
            movie_thoughts=movie.thoughts,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id
        )
    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('fresh_tomatoes.html', 'w')

    # Replace the movie tiles placeholder generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser (in a new tab, if possible)
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)
