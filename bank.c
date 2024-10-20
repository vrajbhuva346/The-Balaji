#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Account {
    int accountNumber;
    char name[100];
    float balance;
};

void createAccount() {
    FILE *fp;
    struct Account acc;

    fp = fopen("accounts.dat", "ab");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return;
    }

    printf("Enter account number: ");
    scanf("%d", &acc.accountNumber);
    printf("Enter account holder name: ");
    scanf("%s", acc.name);
    printf("Enter initial balance: ");
    scanf("%f", &acc.balance);

    fwrite(&acc, sizeof(acc), 1, fp);
    fclose(fp);
    printf("Account created successfully!\n");
}

void displayAccount(int accountNumber) {
    FILE *fp;
    struct Account acc;
    int found = 0;

    fp = fopen("accounts.dat", "rb");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return;
    }

    while (fread(&acc, sizeof(acc), 1, fp)) {
        if (acc.accountNumber == accountNumber) {
            printf("Account Number: %d\n", acc.accountNumber);
            printf("Account Holder Name: %s\n", acc.name);
            printf("Balance: %.2f\n", acc.balance);
            found = 1;
            break;
        }
    }

    fclose(fp);

    if (!found) {
        printf("Account not found!\n");
    }
}

void depositMoney(int accountNumber, float amount) {
    FILE *fp;
    struct Account acc;
    int found = 0;

    fp = fopen("accounts.dat", "rb+");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return;
    }

    while (fread(&acc, sizeof(acc), 1, fp)) {
        if (acc.accountNumber == accountNumber) {
            acc.balance += amount;
            fseek(fp, -sizeof(acc), SEEK_CUR);
            fwrite(&acc, sizeof(acc), 1, fp);
            found = 1;
            break;
        }
    }

    fclose(fp);

    if (found) {
        printf("Amount deposited successfully!\n");
    } else {
        printf("Account not found!\n");
    }
}

void withdrawMoney(int accountNumber, float amount) {
    FILE *fp;
    struct Account acc;
    int found = 0;

    fp = fopen("accounts.dat", "rb+");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return;
    }

    while (fread(&acc, sizeof(acc), 1, fp)) {
        if (acc.accountNumber == accountNumber) {
            if (acc.balance >= amount) {
                acc.balance -= amount;
                fseek(fp, -sizeof(acc), SEEK_CUR);
                fwrite(&acc, sizeof(acc), 1, fp);
                found = 1;
                printf("Amount withdrawn successfully!\n");
            } else {
                printf("Insufficient balance!\n");
            }
            break;
        }
    }

    fclose(fp);

    if (!found) {
        printf("Account not found!\n");
    }
}

void updateAccount(int accountNumber) {
    FILE *fp;
    struct Account acc;
    int found = 0;

    fp = fopen("accounts.dat", "rb+");
    if (fp == NULL) {
        printf("Error opening file!\n");
        return;
    }

    while (fread(&acc, sizeof(acc), 1, fp)) {
        if (acc.accountNumber == accountNumber) {
            printf("Enter new account holder name: ");
            scanf("%s", acc.name);
            fseek(fp, -sizeof(acc), SEEK_CUR);
            fwrite(&acc, sizeof(acc), 1, fp);
            found = 1;
            printf("Account updated successfully!\n");
            break;
        }
    }

    fclose(fp);

    if (!found) {
        printf("Account not found!\n");
    }
}

int main() {
    int choice, accountNumber;
    float amount;

    while (1) {
        printf("\nBank Management System\n");
        printf("1. Create Account\n");
        printf("2. Display Account\n");
        printf("3. Deposit Money\n");
        printf("4. Withdraw Money\n");
        printf("5. Update Account\n");
        printf("6. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                createAccount();
                break;
            case 2:
                printf("Enter account number: ");
                scanf("%d", &accountNumber);
                displayAccount(accountNumber);
                break;
            case 3:
                printf("Enter account number: ");
                scanf("%d", &accountNumber);
                printf("Enter amount to deposit: ");
                scanf("%f", &amount);
                depositMoney(accountNumber, amount);
                break;
            case 4:
                printf("Enter account number: ");
                scanf("%d", &accountNumber);
                printf("Enter amount to withdraw: ");
                scanf("%f", &amount);
                withdrawMoney(accountNumber, amount);
                break;
            case 5:
                printf("Enter account number: ");
                scanf("%d", &accountNumber);
                updateAccount(accountNumber);
                break;
            case 6:
                printf("Exiting...\n");
                return 0;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    }

    return 0;
}
