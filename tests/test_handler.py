import unittest
import index
import projectsLambda

class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        result = index.handler(None, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('Hello World', result['body'])

    def test_projects(self):
        result = projectsLambda.get_projects(None, None)
        print(result)


if __name__ == '__main__':
    unittest.main()
