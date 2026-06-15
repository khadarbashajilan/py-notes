class Payment:
    """
    Base class for payment processing.
    Provides default payment behavior that child classes can override.
    """
    
    def __init__(self, amount):
        """
        Initialize a payment with an amount.
        
        Args:
            amount (float): The payment amount in dollars
        """
        self.amount = amount

    def validate(self):
        """
        Validate if payment details are correct.
        Default implementation always returns True.
        Child classes should override this with specific validation rules.
        
        Returns:
            bool: True if payment is valid, False otherwise
        """
        return True

    def process(self):
        """
        Process the payment transaction.
        Default implementation provides a generic processing message.
        Child classes should override this with payment-specific processing.
        
        Returns:
            str: Message describing the processed payment
        """
        return f"Processing payment of ${self.amount}"


class CreditCardPayment(Payment):
    """
    Payment processing via credit card.
    Inherits from Payment and adds card-specific validation and processing.
    """
    
    def __init__(self, amount, card_number):
        """
        Initialize credit card payment with amount and card number.
        
        Args:
            amount (float): The payment amount in dollars
            card_number (str/int): 16-digit credit card number
        """
        # Call parent's __init__ to set up the amount attribute
        super().__init__(amount)
        self.card_number = card_number

    def process(self):
        """
        Process credit card payment, showing only last 4 digits for security.
        Overrides the parent's process() method with card-specific processing.
        
        Returns:
            str: Message showing amount charged and masked card number
        """
        # Extract last 4 digits for security (mask sensitive data)
        last_four = str(self.card_number)[-4:]
        return f"Charging ${self.amount} to card ending in {last_four}"
    
    def validate(self):
        """
        Validate credit card number format.
        A valid credit card must have exactly 16 digits.
        Overrides the parent's validate() with card-specific rules.
        
        Returns:
            bool: True if card number is 16 digits, False otherwise
        """
        # Convert to string in case card_number is stored as integer
        card_str = str(self.card_number)
        return len(card_str) == 16


class PayPalPayment(Payment):
    """
    Payment processing via PayPal.
    Inherits from Payment and adds email validation and PayPal-specific processing.
    """
    
    def __init__(self, amount, email):
        """
        Initialize PayPal payment with amount and recipient email.
        
        Args:
            amount (float): The payment amount in dollars
            email (str): Recipient's PayPal email address
        """
        # Call parent's __init__ to set up shared attributes
        super().__init__(amount)
        self.email = email

    def process(self):
        """
        Process payment through PayPal.
        Overrides parent's process() with PayPal-specific message format.
        
        Returns:
            str: Message confirming PayPal payment with recipient email
        """
        return f"Sending ${self.amount} via PayPal to {self.email}"

    def validate(self):
        """
        Validate PayPal email format.
        Checks if the email contains '@' symbol (basic validation).
        Overrides parent's validate() with email-specific rules.
        
        Returns:
            bool: True if email contains '@', False otherwise
        """
        # Basic email validation - check for @ symbol
        return "@" in self.email


# ============= TEST CODE =============

# Create a list of different payment types (polymorphism!)
payments = [
    CreditCardPayment(150.00, "1234567890123456"),    # Valid - 16 digits
    CreditCardPayment(75.50, "1234"),                  # Invalid - only 4 digits
    PayPalPayment(200.00, "user@example.com"),         # Valid - has @
    PayPalPayment(50.00, "invalid-email"),             # Invalid - no @
]

print("Processing 4 payments:")

# Loop through all payments using polymorphism
# Each payment validates and processes according to its own class rules
for i, payment in enumerate(payments, 1):
    """
    enumerate(payments, 1) creates pairs: (1, first_payment), (2, second_payment), etc.
    Starting from 1 for human-friendly numbering.
    """
    
    if payment.validate():
        # Payment is valid - process it
        # The correct process() method is called automatically based on the object's class
        print(f"{i}. ✓ {payment.process()}")
    else:
        # Payment is invalid - show specific error based on payment type
        # isinstance() checks what type of payment object we're dealing with
        if isinstance(payment, CreditCardPayment):
            print(f"{i}. ✗ Invalid credit card number")
        elif isinstance(payment, PayPalPayment):
            print(f"{i}. ✗ Invalid PayPal email")
