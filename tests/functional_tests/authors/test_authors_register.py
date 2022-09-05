import pytest
from parameterized import parameterized
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' '*20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)

        return form

    @parameterized.expand([
    ('Ex.: John','Write your first name'),
    ('Ex.: Doe','Write your last name'), #This field must not be empty
    ])
    def test_empty_first_and_last_name_error_message(self,placeholder,error_message):

        def callback(form):

            field = self.get_by_placeholder(form, placeholder)
            field.send_keys(Keys.ENTER)

            form = self.get_form() #when pages is refreshed, it need to get the form again

            self.assertIn(error_message,form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):

        def callback(form):

            last_name_field = self.get_by_placeholder(form, 'Ex.: Doe')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form() #when pages is refreshed, it need to get the form again

            self.assertIn('Write your last name',form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):

        def callback(form):

            username_field = self.get_by_placeholder(form, 'Your username')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form() #when pages is refreshed, it need to get the form again

            self.assertIn('This field must not be empty',form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):

        def callback(form):

            email_field = self.get_by_placeholder(form, 'Your e-mail')
            email_field.clear()
            email_field.send_keys('invalid@invalid')
            email_field.send_keys(Keys.ENTER)
            self.sleep(2)
            form = self.get_form() #when pages is refreshed, it need to get the form again

            self.assertIn('Invalid e-mail',form.text)
        self.form_field_test_with_callback(callback)

    def test_passwords_do_not_match(self):

        def callback(form):

            password_field = self.get_by_placeholder(form, 'Your password')
            password2_field = self.get_by_placeholder(form, 'Repeat your password')

            password_field.clear()
            password_field.send_keys('P@ssw0rd1')

            password2_field.clear()
            password2_field.send_keys('P@ssw0rd1_Diff')

            password2_field.send_keys(Keys.ENTER)
            self.sleep(5)
            form = self.get_form() #when pages is refreshed, it need to get the form again

            self.assertIn('Password and password2 must match!',form.text)
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_sucessfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(form,'Ex.: John').send_keys('First Name')
        self.get_by_placeholder(form,'Ex.: Doe').send_keys('Last Name')
        self.get_by_placeholder(form,'Your username').send_keys('myusername')
        self.get_by_placeholder(form,'Your e-mail').send_keys('email@valid.com')
        self.get_by_placeholder(form,'Your password').send_keys('Penter45')
        self.get_by_placeholder(form,'Repeat your password').send_keys('Penter45')

        form.submit()
        
        self.assertIn(
            'Your user is created, please log in',
            self.browser.find_element(By.TAG_NAME,'body').text
        )
