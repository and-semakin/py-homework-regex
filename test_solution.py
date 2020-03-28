from typing import Tuple

import pytest

from solution import get_full_name, get_phone


class TestSolution:
    @pytest.mark.parametrize(
        ("first_name", "last_name", "surname", "expected_full_name"),
        [
            ("Иванов", "Иван", "Иванович", ("Иванов", "Иван", "Иванович")),
            ("Иванов ", "  Иван", " Иванович ", ("Иванов", "Иван", "Иванович")),
            ("Иванов", "Иван", "", ("Иванов", "Иван", "")),
            ("Иванов", "", "", ("Иванов", "", "")),
            ("Иванов Иван Иванович", "", "", ("Иванов", "Иван", "Иванович")),
            ("Иванов Иван", "", "", ("Иванов", "Иван", "")),
            ("Иванов", "", "", ("Иванов", "", "")),
            ("Иванов  Иван  Иванович", "", "", ("Иванов", "Иван", "Иванович")),
            ("Иванов", "Иван Иванович", "", ("Иванов", "Иван", "Иванович")),
            ("Иванов", "Иван", "", ("Иванов", "Иван", "")),
            ("Иванов", "", "Иван Иванович", ("Иванов", "Иван", "Иванович")),
            ("", "", "Иванов  Иван  Иванович", ("Иванов", "Иван", "Иванович")),
        ],
    )
    def test_returns_expected_output(
        self,
        first_name: str,
        last_name: str,
        surname: str,
        expected_full_name: Tuple[str, str, str],
    ) -> None:
        assert expected_full_name == get_full_name(first_name, last_name, surname)

    @pytest.mark.parametrize(
        ("phone", "expected_phone"),
        [
            ("+74959130037", "+7(495)913-00-37"),
            ("8 495-913-0168", "+7(495)913-01-68"),
            ("+7 (495) 913-04-78", "+7(495)913-04-78"),
            ("+7 (495) 983-36-99 доб. 2926", "+7(495)983-36-99 доб.2926"),
            ("8(495)748-49-73", "+7(495)748-49-73"),
            ("+7 (495) 913-11-11 (доб. 0792)", "+7(495)913-11-11 доб.0792"),
            ("", ""),
            ("  ", ""),
        ],
    )
    def test_return_expected_output(self, phone, expected_phone) -> None:
        assert expected_phone == get_phone(phone)
