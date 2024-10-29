#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TRANSACTIONS 100

typedef struct {
    char description[100];
    float amount;
    char category[50];
} Transaction;

Transaction transactions[MAX_TRANSACTIONS];
int transaction_count = 0;

void add_transaction();
void view_transactions();
void save_to_file();
void load_from_file();

int main() {
    load_from_file();
    int choice;
    while (1) {
        printf("1. Add Transaction\n2. View Transactions\n3. Save & Exit\n");
        scanf("%d", &choice);
        switch (choice) {
            case 1: add_transaction(); break;
            case 2: view_transactions(); break;
            case 3: save_to_file(); exit(0);
        }
    }
    return 0;
}

void add_transaction() {
    if (transaction_count < MAX_TRANSACTIONS) {
        printf("Enter description: ");
        scanf("%s", transactions[transaction_count].description);
        printf("Enter amount: ");
        scanf("%f", &transactions[transaction_count].amount);
        printf("Enter category: ");
        scanf("%s", transactions[transaction_count].category);
        transaction_count++;
    } else {
        printf("Transaction limit reached.\n");
    }
}

void view_transactions() {
    for (int i = 0; i < transaction_count; i++) {
        printf("%s: %.2f (%s)\n", transactions[i].description, transactions[i].amount, transactions[i].category);
    }
}

void save_to_file() {
    FILE *file = fopen("transactions.txt", "w");
    for (int i = 0; i < transaction_count; i++) {
        fprintf(file, "%s %.2f %s\n", transactions[i].description, transactions[i].amount, transactions[i].category);
    }
    fclose(file);
}

void load_from_file() {
    FILE *file = fopen("transactions.txt", "r");
    if (file) {
        while (fscanf(file, "%s %f %s", transactions[transaction_count].description, &transactions[transaction_count].amount, transactions[transaction_count].category) == 3) {
            transaction_count++;
        }
        fclose(file);
    }
}
