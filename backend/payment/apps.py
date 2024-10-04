from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payment'

    def ready(self):
        """
        Prepare the application by importing payment signals.
        
        This method is called by Django when the application is fully loaded and ready to serve requests.
        It imports the signals module from the payment app to ensure that all signal handlers are registered.
        
        Args:
            self: The instance of the application configuration class.
        
        Returns:
            None: This method doesn't return anything.
        """
        import payment.signals 