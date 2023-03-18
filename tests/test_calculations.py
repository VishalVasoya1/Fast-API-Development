import pytest
from app.calculations import add, multiply, substract, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected",[
    (3,5,8),
    (10,15,25),
    (45,23,68)
])
def test_add(num1, num2, expected):
    print('Testing add Function')
    sum = add(num1,num2)
    assert sum == expected

def test_multiply():
    print('Testing multiply Function')
    multi = multiply(5,3)
    assert multi == 15


def test_divide():
    print('Testing divide Function')
    div = divide(15,3)
    assert div == 5

def test_bank_zero_initial_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 100