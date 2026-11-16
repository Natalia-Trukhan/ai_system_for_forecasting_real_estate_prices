from matplotlib import pyplot as plt

from model_train import model_1, x_test, model_2, y_test


def make_plots(model_choice_widget):
    # Імпортуємо інтерфейс локально всередині функції, щоб уникнути циклічного імпорту

    selected_model = model_choice_widget.get()
    if "Лінійна" in selected_model:
        y_pred = model_1.predict(x_test)
        title_prefix = "Linear Regression"
    else:
        y_pred = model_2.predict(x_test)
        title_prefix = "Decision Tree"

    # Створюємо вікно з 2 графіками поруч
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Графік 1: Порівняння прогнозованих і фактичних цін
    axes[0].scatter(y_test[:500], y_pred[:500], alpha=0.6, color="blue", edgecolors="k")
    axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    axes[0].set_title(f"{title_prefix}: Фактичні vs Прогнозовані ціни")
    axes[0].set_xlabel("Фактична ціна ($100k)")
    axes[0].set_ylabel("Прогнозована ціна ($100k)")
    axes[0].grid(True)

    # Графік 2: Розподіл похибок
    errors = y_test - y_pred
    axes[1].hist(errors, bins=30, color="orange", edgecolor="black", alpha=0.7)
    axes[1].axvline(0, color='red', linestyle='dashed', linewidth=2)
    axes[1].set_title(f"{title_prefix}: Розподіл похибок")
    axes[1].set_xlabel("Похибка прогнозу ($100k)")
    axes[1].set_ylabel("Кількість об'єктів")
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()
