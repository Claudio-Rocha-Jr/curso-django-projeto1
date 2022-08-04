# from django.test import TestCase
from unittest import TestCase
from urllib import response

from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    
    @parameterized.expand([
        ('username','Your username'),
        ('email','Your e-mail'),
        ('first_name','Ex.: John'),
        ('last_name','Ex.: Doe'),
        ('password','Your password'),
        ('password2','Repeat your password'),
    ])
    def test_fields_placeholders(self, field, placeholder):
        form = RegisterForm ()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder,current_placeholder)

    @parameterized.expand([
        ('password','Password must be strong'),
        ('password2','Password must be strong'),
        ('email','The e-mail must be valid'),
        ('username','Username must have letters, number or one of these @.+-'),
    ])
    def test_fields_helptext(self, field, help_text):
        form = RegisterForm ()
        current_help_text = form[field].field.help_text
        self.assertEqual(help_text,current_help_text)

    @parameterized.expand([
        ('username', 'Username'), #Change field label
        ('first_name','First Name'), 
        ('last_name', 'Last Name'),
        ('email','E-mail'),
        ('password','Password'),
        ('password2','Password2'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm ()
        current_label = form[field].field.label
        self.assertEqual(label,current_label)

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self,*args,**kwargs):
        self.form_data = {
            'username':'user',
            'first_name':'first',
            'last_name':'last',
            'email':'email@anyemail.com',
            'password':'Str0ngP@assword1',
            'password2':'Str0ngP@assword1'
        }
        return super().setUp(*args,**kwargs)

    @parameterized.expand([
        ('username','This field must not be empty'),
        ('first_name','Write your first name'),
        ('last_name','Write your last name'),
        ('password','Type your password'),
        ('password2','Passwords must match'),
        ('email','E-mail must not be empty'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)
        # self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get(field))


    def test_fields_cannot_be_less_than_3_characters(self):

        msg = 'Username must have at least 4 characters'

        self.form_data['username'] = 'Joa'
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)
        self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('username'))
 
    def test_fields_cannot_be_greater_than_150_characters(self):

        msg = 'This field must have less or equal than 150 characters'

        self.form_data['username'] = 'A'*151
        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)
        #self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):

        self.form_data['password'] = 'abc'

        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)

        msg = 'Password failed regex'

        #self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('password'))

        self.form_data['password'] = 'Abc123456'

        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)

        self.assertNotIn(msg,response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):

        self.form_data['password'] = 'Abc123456'
        self.form_data['password2'] = 'Abc1234567'

        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)

        msg = 'Password and password2 must match!'

        #self.assertIn(msg,response.content.decode('utf-8'))
        self.assertIn(msg,response.context['form'].errors.get('password'))
        self.assertIn(msg,response.context['form'].errors.get('password2'))

        self.form_data['password'] = 'Abc123456'
        self.form_data['password2'] = 'Abc123456'

        url = reverse('authors:create')
        response = self.client.post(url,data=self.form_data, follow=True)

        self.assertNotIn(msg,response.content.decode('utf-8'))
        #self.assertNotIn(msg,response.context['form'].errors.get('password2'))

    def test_send_get_request_to_registration_create_view_returns_404(self):

        url = reverse('authors:create')
        response = self.client.get(url)

        self.assertEqual(404,response.status_code)

    def test_if_email_can_not_be_repeated(self):

        url = reverse('authors:create')

        self.client.post(url,data=self.form_data, follow=True)

        response = self.client.post(url,data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'
        self.assertIn(msg,response.context['form'].errors.get('email'))

