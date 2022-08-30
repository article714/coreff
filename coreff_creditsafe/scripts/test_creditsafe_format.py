import requests
import json
import getpass


class TestCreditSafe:
    def __init__(self, url, username, password, nb_company=3) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.nb_company = nb_company

    def check_companies(self, companies):
        assert len(companies) == self.nb_company
        for c in companies:
            assert isinstance(c["id"], str)
            assert isinstance(c["name"], str)
            assert isinstance(c["regNo"], str)
            assert isinstance(c["address"], dict)
            assert isinstance(c["country"], str)
            assert (
                not "vatNo" in c
                or isinstance(c["vatNo"], str)
                or (
                    isinstance(c["vatNo"], list)
                    and isinstance(c["vatNo"][0], str)
                )
            )
            assert not "phoneNumbers" in c or (
                isinstance(c["phoneNumbers"], list)
                and isinstance(c["phoneNumbers"][0], str)
            )

    def assert_company(self, company, fields, last_type=str):
        data = company
        for i in range(len(fields)):
            field = fields[i]
            if field not in data:
                break
            assert isinstance(
                data[field], last_type if (i == len(fields) - 1) else dict
            )
            data = data[field]

    def check_company(self, company):
        self.assert_company(
            company,
            [
                "shareCapitalStructure",
                "nominalShareCapital",
                "value",
            ],
            int,
        )
        self.assert_company(
            company,
            [
                "creditScore",
                "currentCreditRating",
                "creditLimit",
                "value",
            ],
        )
        self.assert_company(
            company,
            [
                "companySummary",
                "businessName",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "legalForm",
                "description",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "companyRegistrationNumber",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "commercialCourt",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "companyRegistrationDate",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "principalActivity",
                "code",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "principalActivity",
                "description",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "country",
            ],
        )
        self.assert_company(
            company,
            [
                "companyIdentification",
                "basicInformation",
                "companyStatus",
                "status",
            ],
        )
        self.assert_company(
            company,
            [
                "creditScore",
                "currentCreditRating",
                "providerValue",
                "value",
            ],
        )
        self.assert_company(
            company,
            [
                "creditScore",
                "currentCreditRating",
                "providerValue",
                "maxValue",
            ],
        )
        self.assert_company(
            company,
            [
                "creditScore",
                "currentCreditRating",
                "commonDescription",
            ],
        )
        self.assert_company(
            company,
            [
                "creditScore",
                "currentCreditRating",
                "providerDescription",
            ],
        )
        self.assert_company(
            company,
            [
                "creditScore",
                "latestRatingChangeDate",
            ],
        )
        self.assert_company(
            company,
            [
                "directors",
                "currentDirectors",
            ],
            list,
        )

    def get_token(self):
        data = {"username": self.username, "password": self.password}
        res = requests.post(f"{self.url}/authenticate", data=json.dumps(data))
        return res.json()["token"]

    def get_companies(self, token, country):
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "language": "en",
            "page": 1,
            "pageSize": self.nb_company,
            "countries": country,
            "name": "Inf",
        }
        res = requests.get(
            f"{self.url}/companies", headers=headers, params=params
        )
        return res.json()["companies"]

    def get_company(self, token, company):
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "language": "en",
        }
        res = requests.get(
            f"{self.url}/companies/{company}", headers=headers, params=params
        )
        return res.json()["report"]

    def test_companies(self, country_list):
        token = self.get_token()
        for country in country_list:
            print(f"Run country {country} ...")
            companies_data = self.get_companies(token, country)
            self.check_companies(companies_data)
            for c in companies_data:
                company_data = self.get_company(token, c["id"])
                self.check_company(company_data)


if __name__ == "__main__":
    u = input("URL : ")
    usr = input("USR : ")
    pwd = getpass.getpass("PWD : ")
    c = input("COUNTRIES : ")
    c = c.split(",")
    TestCreditSafe(u, usr, pwd).test_companies(c)
    print("Test passed")
