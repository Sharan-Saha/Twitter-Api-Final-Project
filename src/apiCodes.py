
class Codes:
    def __init__(self):
        """
        initializes the variables for the twitter API tokens
        args: none
        returns: none
        """
        self.api_key  = ""
        self.api_key_scrt  = ""
        self.bearer_tkn  = ""
        self.access_tkn  = ""
        self.access_tkn_scrt = ""
        
    def assignValues(self):
        """
        assigns tokens to the token variables
        args: none
        return: none
        """
        self.api_key = "dlUfoR1cP3KWse05efRrm262C"
        self.api_key_scrt = "z0JXIs8pUGFG9Lp1LB4B6VHJVG0L90ZnMuAupR3PGViOxIYjf6"
        self.bearer_tkn = "AAAAAAAAAAAAAAAAAAAAAMUlUwEAAAAAupkdvEh16A%2FbM36uhHL%2BoZ%2FT%2Fa4%3Dh6dgHFVGzy1CtVr5iXywd5VAWuTVIfgCu25hkfwKbSinapQAdG"
        self.access_tkn = "1067612118675943424-C45qGUQP327ro5uQydYe51WiVHRhTi"
        self.access_tkn_scrt = "LHxW4HEtB6M0UNRy8SbSUmN0ssCFtVCEXWaUFpMsaJ74B"
        return {"api_key": self.api_key, "api_key_scrt": self.api_key_scrt, "access_tkn": self.access_tkn, "access_tkn_scrt" : self.access_tkn_scrt}
