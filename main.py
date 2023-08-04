class Product:
    """
    Represents a product in the store.

    Attributes:
       name (str): The name of the product.
       price (float): The price of the product.
    """

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"


class ShoppingCart:
    """
   Represents a shopping cart to manage items added by the BargainHunter customer.

   Attributes:
       items (dict): A dictionary to store products and their quantities in the cart.
   """

    def __init__(self):
        self.items = {}

    def add_product(self, product, quantity=1):
        """
        Add a product to the shopping cart or increase its quantity if already present.

        Args:
            product (Product): The product to add to the cart.
            quantity (int, optional): The quantity of the product to add. Defaults to 1.
        """
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity

    def remove_product(self, product, quantity=1):
        """
        Remove a product from the shopping cart or decrease its quantity if present.

        Args:
            product (Product): The product to remove from the cart.
            quantity (int, optional): The quantity of the product to remove. Defaults to 1.
        """
        if product in self.items:
            self.items[product] -= quantity
            if self.items[product] <= 0:
                del self.items[product]

    def __str__(self):
        total_amount = sum(product.price * quantity for product, quantity in self.items.items())
        cart_content = "\n".join(f"{product} - Quantity: {quantity}" for product, quantity in self.items.items())
        return f"Shopping Cart:\n{cart_content}\nTotal amount: ${total_amount:.2f}"


class Customer:
    """
    Represents a generic customer.

    Attributes:
        name (str): The name of the customer.
    """

    def __init__(self, name):
        self.name = name


class LoyalCustomer(Customer):
    """
    Represents a loyal customer who can buy exclusive products.

    Attributes:
        name (str): The name of the loyal customer.
        exclusive_products (dict): A dictionary to store exclusive products and their quantities.
    """

    def __init__(self, name):
        super().__init__(name)
        self.exclusive_products = {}

    def add_exclusive_product(self, product, quantity=1):
        """
        Add an exclusive product to the customer's list or increase its quantity if already present.

        Args:
            product (Product): The exclusive product to add to the customer's list.
            quantity (int, optional): The quantity of the product to add. Defaults to 1.
        """
        if product in self.exclusive_products:
            self.exclusive_products[product] += quantity
        else:
            self.exclusive_products[product] = quantity

    def remove_exclusive_product(self, product, quantity=1):
        """
        Remove an exclusive product from the customer's list or decrease its quantity if present.

        Args:
            product (Product): The exclusive product to remove from the customer's list.
            quantity (int, optional): The quantity of the product to remove. Defaults to 1.
        """
        if product in self.exclusive_products:
            self.exclusive_products[product] -= quantity
            if self.exclusive_products[product] <= 0:
                del self.exclusive_products[product]

    def __str__(self):
        exclusive_content = "\n".join(f"{product} - Quantity: {quantity}"
                                      for product, quantity in self.exclusive_products.items())
        return f"Loyal Customer: {self.name}\nExclusive Products:\n{exclusive_content}"


class BargainHunter(Customer):
    """
    Represents a bargain hunter customer who can buy any other products listed from low to high price.

    Attributes:
        name (str): The name of the bargain hunter customer.
        shopping_cart (ShoppingCart): The shopping cart for the bargain hunter.
    """

    def __init__(self, name):
        super().__init__(name)
        self.shopping_cart = ShoppingCart()

    def add_to_cart(self, product, quantity=1):
        """
        Add a product to the shopping cart.

        Args:
            product (Product): The product to add to the cart.
            quantity (int, optional): The quantity of the product to add. Defaults to 1.
        """
        self.shopping_cart.add_product(product, quantity)

    def remove_from_cart(self, product, quantity=1):
        """
        Remove a product from the shopping cart.

        Args:
            product (Product): The product to remove from the cart.
            quantity (int, optional): The quantity of the product to remove. Defaults to 1.
        """
        self.shopping_cart.remove_product(product, quantity)

    def __str__(self):
        return f"Bargain Hunter: {self.name}\n{self.shopping_cart}"


def main():
    customer = None
    products = [
        Product("Shirt", 20.0),
        Product("Pants", 30.0),
        Product("Shoes", 50.0),
        Product("Hat", 15.0),
    ]

    while True:
        print("\n===== Command Line Menu =====")
        print("1. Create a customer")
        print("2. List products")
        print("3. Add/remove a product to the shopping cart")
        print("4. See current shopping cart")
        print("5. Checkout")
        print("0. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 0:
            print("Thank you for using the shopping cart application. Goodbye!")
            break

        elif choice == 1:
            name = input("Enter customer name: ")
            customer_type = input("Enter customer type (Loyal/Bargain): ").lower()
            if customer_type == "loyal":
                customer = LoyalCustomer(name)
            elif customer_type == "bargain":
                customer = BargainHunter(name)
            else:
                print("Invalid customer type. Please choose 'Loyal' or 'Bargain'.")

        elif choice == 2:
            print("\n===== Available Products =====")
            for i, product in enumerate(products, start=1):
                print(f"{i}. {product}")

        elif choice == 3:
            if customer is None:
                print("Please create a customer first (Option 1).")
            else:
                # Display the available products for the customer to choose from
                print("\n===== Available Products =====")
                for i, product in enumerate(products, start=1):
                    print(f"{i}. {product}")

                product_index = int(input("Enter product index to add/remove (0 to cancel): "))
                if product_index == 0:
                    continue

                product_index -= 1  # Adjust for 0-based indexing
                if 0 <= product_index < len(products):
                    product = products[product_index]
                    quantity = int(input(f"Enter the quantity of '{product.name}' to add/remove: "))
                    if quantity < 0:
                        print("Invalid quantity. Quantity must be non-negative.")
                    else:
                        if isinstance(customer, LoyalCustomer):
                            customer.add_exclusive_product(product, quantity)
                        else:
                            customer.add_to_cart(product, quantity)
                else:
                    print("Invalid product index. Please choose a valid product.")

        elif choice == 4:
            if customer is None:
                print("Please create a customer first (Option 1).")
            else:
                # Display the customer's information based on their type (LoyalCustomer or BargainHunter)
                if isinstance(customer, LoyalCustomer):
                    print(customer)
                else:
                    # For BargainHunter, display their shopping cart directly
                    print(customer.shopping_cart)

        elif choice == 5:
            if customer is None:
                print("Please create a customer first (Option 1).")
            else:
                # Perform the checkout based on the customer type (LoyalCustomer or BargainHunter)
                if isinstance(customer, LoyalCustomer):
                    if len(customer.exclusive_products) == 0:
                        print("You need to add products to the shopping cart before checkout.")
                    else:
                        print("\n===== Checkout =====")
                        print(customer)
                        confirm = input("Confirm checkout? (yes/no): ")
                        if confirm.lower() == "yes":
                            print("Thank you for your purchase!")
                            break
                        else:
                            print("Checkout canceled. Continue shopping.")
                else:
                    if len(customer.shopping_cart.items) == 0:
                        print("You need to add products to the shopping cart before checkout.")
                    else:
                        print("\n===== Checkout =====")
                        print(customer)
                        confirm = input("Confirm checkout? (yes/no): ")
                        if confirm.lower() == "yes":
                            print("Thank you for your purchase!")
                            break
                        else:
                            print("Checkout canceled. Continue shopping.")

        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
