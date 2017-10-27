import webbrowser
import csv


class Movie():
    """ Create an instance of the class `Movie`.

        Creates an instance of the class `Movie` which will be used in a
        dynamically populated movie trailer website.

        Args:
            movie_title: A movie title
            movie_year: The year the movie was made
            movie_storyline: A short official summary of the movie from
            IMDb
            movie_thoughts: Some personal reflections on the movie
            poster_image: A URL path to an image of the movie
            trailer_youtube: A URL to the youtube trailer of the movie
    """
    def __init__(self, movie_title, movie_year, movie_storyline,
                 movie_thoughts, poster_image, trailer_youtube):
        self.title = movie_title
        self.year = movie_year
        self.storyline = movie_storyline
        self.thoughts = movie_thoughts
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        """Open YouTube URL in web browser."""
        webbrowser.open(self.trailer_youtube_url)


def csv_dict_list(csv_file):
    """Create a list of dictionaries from a csv file.

        Takes a csv file as its argument and appends each row from the
        file to a list. Each row of the file is a dictionary where the
        values in first row become the keys to each dictionary.

        Args:
            csv_file: A csv file path

        Returns:
            dict_list: A list of dictionaries mapping the keys to the
            corresponding table row data. For example:

                [
                    {
                        'poster': 'https://goo.gl/4yna4o',
                        'summary': 'A kick-ass lady outwits the dudes.',
                        'title': 'Jackie Brown',
                        'trailer': 'https://youtu.be/J9Bd4ShuEAw',
                        'year': '1997',
                        'yw-thoughts': 'Awesome movie, thumbs up!'
                    },
                    {
                        'poster': 'https://goo.gl/sERJr1',
                        'summary': "A battle between several faction in magical
                         woods.",
                        'title': 'Princess Mononoke',
                        'trailer': 'https://youtu.be/YOuG8m2RqOs',
                        'year': '1999',
                        'yw-thoughts': 'This movie is beautiful.'
                    }
                ]
    """
    reader = csv.DictReader(open(csv_file, 'rb'))

    dict_list = []
    for row in reader:
        dict_list.append(row)
    return dict_list
