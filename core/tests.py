from django.test import TestCase
from core.models import Account

from core.services import BankAccountServices


class Request:
    data: dict
    query_params: dict

    def __init__(self, data=None, query_params=None):
        self.data = data
        self.query_params = query_params


class CreateBankAccountTest(TestCase):
    def setUp(self):
        self.request = Request(data={"number": "1", "balance": 1000})
        self.bank_account_service = BankAccountServices()

    def test_create_default_account_bank(self):
        self.request.data["type"] = Account.TypeChoices.DEFAULT

        response_message, response_status = self.bank_account_service.create_account_service(
            self.request)
        self.assertEqual(response_status, 201)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(response_message['type'], Account.TypeChoices.DEFAULT)
        self.assertEqual(float(response_message['balance']), 1000)
        self.assertEqual(response_message['score'], None)

    def test_create_bonus_account_bank(self):
        self.request.data["type"] = Account.TypeChoices.BONUS

        response_message, response_status = self.bank_account_service.create_account_service(
            self.request)
        self.assertEqual(response_status, 201)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(response_message['type'], Account.TypeChoices.BONUS)
        self.assertEqual(float(response_message['balance']), 1000)
        self.assertEqual(response_message['score'], 10)

    def test_create_savings_account_bank(self):
        self.request.data["type"] = Account.TypeChoices.SAVINGS

        response_message, response_status = self.bank_account_service.create_account_service(
            self.request)
        self.assertEqual(response_status, 201)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(response_message['type'], Account.TypeChoices.SAVINGS)
        self.assertEqual(float(response_message['balance']), 1000)
        self.assertEqual(response_message['score'], None)


class GetAccountBankAndBalanceTest(TestCase):
    def setUp(self):
        self.create_default_account_request = Request()
        self.create_bonus_account_request = Request()
        self.create_savings_account_request = Request()
        self.request = Request()
        self.bank_account_service = BankAccountServices()

        self.create_default_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        self.create_bonus_account_request.data = {
            "number": "2",
            "type": Account.TypeChoices.BONUS,
            "balance": 2000
        }

        self.create_savings_account_request.data = {
            "number": "3",
            "type": Account.TypeChoices.SAVINGS,
            "balance": 2000
        }

        self.bank_account_service.create_account_service(
            self.create_default_account_request)
        self.bank_account_service.create_account_service(
            self.create_bonus_account_request)
        self.bank_account_service.create_account_service(
            self.create_savings_account_request)

    def test_get_default_account_bank_and_balance(self):
        self.request.query_params = {
            "account_number": "1"
        }

        response_message, response_status = self.bank_account_service.check_ballance_and_get_account_service(
            self.request
        )
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")

    def test_get_bonus_account_bank_and_balance(self):
        self.request.query_params = {
            "account_number": "2"
        }

        response_message, response_status = self.bank_account_service.check_ballance_and_get_account_service(
            self.request
        )
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "2")

    def test_get_savings_account_bank_and_balance(self):
        self.request.query_params = {
            "account_number": "3"
        }

        response_message, response_status = self.bank_account_service.check_ballance_and_get_account_service(
            self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "3")


class CreditAccountBankTest(TestCase):
    def setUp(self):
        self.create_default_account_request = Request()
        self.create_bonus_account_request = Request()
        self.create_savings_account_request = Request()
        self.request = Request()
        self.bank_account_service = BankAccountServices()

        self.create_default_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        self.create_bonus_account_request.data = {
            "number": "2",
            "type": Account.TypeChoices.BONUS,
            "balance": 2000
        }

        self.bank_account_service.create_account_service(
            self.create_default_account_request)
        self.bank_account_service.create_account_service(
            self.create_bonus_account_request)

    def test_credit_default_account(self):
        self.request.data = {
            "number": "1",
            "amount": 1000
        }

        response_message, response_status = self.bank_account_service.credit_account_service(
            self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(float(response_message['balance']), 3000)

    def test_credit_with_negative_number(self):
        self.request.data = {
            "number": "1",
            "amount": -1000
        }

        _, response_status = self.bank_account_service.credit_account_service(
            self.request)
        self.assertEqual(response_status, 400)

    def test_credit_bonus_account(self):
        self.request.data = {
            "number": "2",
            "amount": 1000
        }

        response_message, response_status = self.bank_account_service.credit_account_service(
            self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "2")
        self.assertEqual(float(response_message['balance']), 3000)
        self.assertEqual(response_message['score'], 20)


class DebitAccountBankTest(TestCase):
    def setUp(self):
        self.create_default_account_request = Request()
        self.create_bonus_account_request = Request()
        self.create_savings_account_request = Request()
        self.request = Request()
        self.bank_account_service = BankAccountServices()

        self.create_default_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        self.bank_account_service.create_account_service(
            self.create_default_account_request)

    def test_debit_default_account(self):
        self.request.data = {
            "number": "1",
            "amount": 1000
        }

        response_message, response_status = self.bank_account_service.debit_account_service(
            self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(response_message['number'], "1")
        self.assertEqual(float(response_message['balance']), 1000)

    def test_debit_with_negative_number(self):
        self.request.data = {
            "number": "1",
            "amount": -1000
        }

        _, response_status = self.bank_account_service.debit_account_service(
            self.request)
        self.assertEqual(response_status, 400)

    def test_debit_more_than_account_ballance(self):
        self.request.data = {
            "number": "1",
            "amount": 4000
        }

        _, response_status = self.bank_account_service.debit_account_service(
            self.request)
        self.assertEqual(response_status, 400)


class TransferAccountBankTest(TestCase):
    def setUp(self):
        self.create_default_account_request = Request()
        self.create_bonus_account_request = Request()
        self.create_savings_account_request = Request()
        self.request = Request()
        self.bank_account_service = BankAccountServices()

        self.create_default_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.DEFAULT,
            "balance": 2000
        }

        self.create_bonus_account_request.data = {
            "number": "2",
            "type": Account.TypeChoices.BONUS,
            "balance": 2000
        }

        self.bank_account_service.create_account_service(
            self.create_default_account_request)
        self.bank_account_service.create_account_service(
            self.create_bonus_account_request)

    def test_transfer_with_negative_amount(self):
        self.request.data = {
            "origin_number": "1",
            "destination_number": "2",
            "amount": -1000
        }

        _, response_status = self.bank_account_service.transfer_between_accounts(
            self.request)
        self.assertEqual(response_status, 400)

    def test_transfer_with_negative_balance(self):
        self.request.data = {
            "origin_number": "1",
            "destination_number": "2",
            "amount": 3000
        }

        _, response_status = self.bank_account_service.transfer_between_accounts(
            self.request)
        self.assertEqual(response_status, 400)

    def test_transfer_to_bonus_account(self):
        self.request.data = {
            "origin_number": "1",
            "destination_number": "2",
            "amount": 1500
        }

        response_message, response_status = self.bank_account_service.transfer_between_accounts(
            self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(len(response_message), 2)
        self.assertEqual(response_message[0]["number"], "1")
        self.assertEqual(response_message[1]["number"], "2")
        self.assertEqual(float(response_message[1]["balance"]), 3500)
        self.assertEqual(response_message[1]["score"], 20)


class YieldInterestAccountBankTest(TestCase):
    def setUp(self):
        self.create_savings_account_request = Request()
        self.request = Request()
        self.bank_account_service = BankAccountServices()

        self.create_savings_account_request.data = {
            "number": "1",
            "type": Account.TypeChoices.SAVINGS,
            "balance": 2000
        }

        self.bank_account_service.create_account_service(
            self.create_savings_account_request)

    def test_transfer_with_negative_amount(self):
        self.request.data = {
            "number": "1",
            "interest_percentage": 10
        }

        response_message, response_status = self.bank_account_service.yield_interest_account(
            self.request)
        self.assertEqual(response_status, 200)
        self.assertEqual(float(response_message["balance"]), 2200)
