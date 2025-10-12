# ===========================
# Feature and Target Names
# ===========================


class BankFeatures:
    """Column names for Bank Marketing dataset features"""

    AGE = "age"
    # Age of the person (numerical)
    JOB = "job"
    # type of job (categorical: "admin.","unknown","unemployed","management","housemaid","entrepreneur","student", "blue-collar","self-employed","retired","technician","services")
    MARITAL = "marital"
    # marital status (categorical: "married","divorced","single"; note: "divorced" means divorced or widowed)
    EDUCATION = "education"
    # type of education (categorical: "unknown","secondary","primary","tertiary")
    DEFAULT = "default"  #
    # has credit in default? (binary: "yes","no")
    BALANCE = "balance"  #
    # average yearly balance, in euros (numeric)
    HOUSING = "housing"  #
    # has housing loan? (binary: "yes","no")
    LOAN = "loan"  #
    # has personal loan? (binary: "yes","no")
    CONTACT = "contact"  #
    # contact communication type (categorical: "unknown","telephone","cellular")
    DAY = "day"  #
    # last contact day of the month (numeric)
    MONTH = "month"  #
    # last contact month of year (categorical: "jan", "feb", "mar", ..., "nov", "dec")
    DURATION = "duration"  #
    # last contact duration, in seconds (numeric)
    CAMPAIGN = "campaign"  #
    # number of contacts performed during this campaign and for this client (numeric, includes last contact)
    PDAYS = "pdays"  #
    # number of days that passed by after the client was last contacted from a previous campaign (numeric, -1 means client was not previously contacted)
    PREVIOUS = "previous"  #
    # number of contacts performed before this campaign and for this client (numeric)
    POUTCOME = "poutcome"  #
    # outcome of the previous marketing campaign (categorical: "unknown","other","failure","success")


class BankTarget:
    """Target variable for classification"""

    SUBSCRIBED = "y"
    # has the client subscribed a term deposit? (binary: "yes","no")
