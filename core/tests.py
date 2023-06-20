from django.test import TestCase
from core.models import Account

from core.services import BankAccountServices

class Request:
    data: dict
    query_params: dict

class CreateBankAccountTest(TestCase):
    def setUp(self):
        self.request = Request()

    def test_create_default_account_bank(self):
        bank_account_service = BankAccountServices()

        self.request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 1000
        }

        response_message, response_status = bank_account_service.create_account_service(self.request)
        self.assertEqual(response_status, 201)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(response_message['type'], Account.TypeChoices.DEFAULT)
        self.assertEqual(float(response_message['balance']), 1000)
        self.assertEqual(response_message['score'], None)
    
    def test_create_bonus_account_bank(self):
        bank_account_service = BankAccountServices()

        self.request.data = {
            "number": "1",
            "type": Account.TypeChoices.BONUS,
            "balance": 1000
        }

        response_message, response_status = bank_account_service.create_account_service(self.request)
        self.assertEqual(response_status, 201)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(response_message['type'], Account.TypeChoices.BONUS)
        self.assertEqual(float(response_message['balance']), 1000)
        self.assertEqual(response_message['score'], 10)
    
    def test_create_savings_account_bank(self):
        bank_account_service = BankAccountServices()

        self.request.data = {
            "number": "1",
            "type": Account.TypeChoices.SAVINGS,
            "balance": 1000
        }

        response_message, response_status = bank_account_service.create_account_service(self.request)
        self.assertEqual(response_status, 201)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(response_message['type'], Account.TypeChoices.SAVINGS)
        self.assertEqual(float(response_message['balance']), 1000)
        self.assertEqual(response_message['score'], None)



class GetAccountBankAndBalanceTest(TestCase):
    def setUp(self):
        self.create_account_request = Request()
        self.request = Request()
    
    def test_get_default_account_bank_and_balance(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.query_params = {
            "account_number": "1"
        }

        response_message, response_status = bank_account_service.check_ballance_and_get_account_service(self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
    
    def test_get_bonus_account_bank_and_balance(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.BONUS,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.query_params = {
            "account_number": "1"
        }

        response_message, response_status = bank_account_service.check_ballance_and_get_account_service(self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
    
    def test_get_savings_account_bank_and_balance(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.SAVINGS,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.query_params = {
            "account_number": "1"
        }

        response_message, response_status = bank_account_service.check_ballance_and_get_account_service(self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")

class CreditAccountBankTest(TestCase):
    def setUp(self):
        self.create_account_request = Request()
        self.request = Request()
    
    def test_credit_default_account(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.data = {
            "number": "1",
            "amount": 1000
        }

        response_message, response_status = bank_account_service.credit_account_service(self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(float(response_message['balance']), 3000)

    def test_credit_with_negative_number(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.data = {
            "number": "1",
            "amount": -1000
        }

        _, response_status = bank_account_service.credit_account_service(self.request)
        self.assertEqual(response_status, 400)
    
    def test_credit_bonus_account(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.BONUS,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.data = {
            "number": "1",
            "amount": 1000
        }

        response_message, response_status = bank_account_service.credit_account_service(self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(float(response_message['balance']), 3000)
        self.assertEqual(response_message['score'], 20)

class DebitAccountBankTest(TestCase):
    def setUp(self):
        self.create_account_request = Request()
        self.request = Request()
    
    def test_debit_default_account(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.data = {
            "number": "1",
            "amount": 1000
        }

        response_message, response_status = bank_account_service.debit_account_service(self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(float(response_message['balance']), 1000)
    
    def test_debit_with_negative_number(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.data = {
            "number": "1",
            "amount": -1000
        }

        _, response_status = bank_account_service.debit_account_service(self.request)
        self.assertEqual(response_status, 400)
    
    def test_debit_more_than_account_ballance(self):
        bank_account_service = BankAccountServices()

        create_account_request = Request()
        create_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        bank_account_service.create_account_service(create_account_request)

        self.request.data = {
            "number": "1",
            "amount": 4000
        }

        _, response_status = bank_account_service.debit_account_service(self.request)
        self.assertEqual(response_status, 400)