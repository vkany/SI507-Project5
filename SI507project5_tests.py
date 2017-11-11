import unittest
from SI507project5_code import *

class Project5(unittest.TestCase):
    def setUp(self):
        self.test_DETdict = get_response_diction('Music','Detroit')
        self.test_NYdict = get_response_diction('Art Show','New York')
        self.url = 'https://www.eventbriteapi.com/v3'


    def test_caching(self):
        self.assertFalse(len(CACHE_DICTION) is len([]))
        # Testing to see if data gets cached

    def test_token(self):
        self.assertEqual(get_saved_token(),{"access_token": "KUNBVEXGQGEXPISENRY6", "token_type": "bearer"})
        #testing if the token that we get is correctly saved

    def test_event_names(self):
        self.assertEqual(type(self.test_NYdict),type({}))
        self.assertEqual(self.test_NYdict["events"][0]["name"]["text"],"Comedy at the Lantern")
        self.assertEqual(self.test_DETdict["events"][1]["name"]["text"],"FireHouse One Year Celebration")
    #testing the names are stored correctly

    def test_location(self):
        for events in self.test_NYdict["events"]:
            self.assertEqual(self.test_NYdict["location"]["augmented_location"]["city"],'New York')
        for events in self.test_DETdict["events"]:
            self.assertEqual(self.test_DETdict["location"]["augmented_location"]["city"],'Detroit')
    #testing the location of all events is in the city we wanted

    def test_description_type(self):
        for events in self.test_NYdict["events"]:
            self.assertEqual(type(event["description"]["text"]),str)
        for events in self.test_DETdict["events"]:
            self.assertEqual(type(event["description"]["text"]),str)
    #testing the description of all events is recieving a string format for our csv


    def tearDown(self):
        pass










if __name__ == "__main__":
    unittest.main(verbosity=2)
