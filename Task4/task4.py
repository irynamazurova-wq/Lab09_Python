import pandas as pd
import matplotlib.pyplot as plt
import os

class KmrCsv:
    ref = None
    num = 0

    def set_ref(self, ref):
        self.ref = ref

    def get_ref(self):
        return self.ref

    def set_num(self, num):
        self.num = num

    def read_csv(self):
        if self.ref and os.path.exists(self.ref):
            self.df = pd.read_csv(self.ref)
            return self.df
        else:
            print(f"Помилка: Файл '{self.ref}' не знайдено.")
            return None

    def file_info(self):
        if hasattr(self, 'df'):
            print(f"Інфо: КМР №{self.num}. Кількість студентів: {len(self.df)}")
        else:
            print("Дані ще не прочитано.")


class Statistic:
    def avg_stat(self):
        q_cols = [col for col in self.df.columns if col.startswith('q')]
        means = self.df[q_cols].mean() * 100
        return tuple(means)

    def marks_stat(self):
        return self.df['grade'].value_counts().to_dict()

    def marks_per_time(self):
        result = {}
        for index, row in self.df.iterrows():
            score_per_min = row['grade'] / row['time'] if row['time'] > 0 else 0
            result[row['id']] = round(score_per_min, 2)
        return result

    def best_marks_per_time(self, bottom_margin, top_margin):
        filtered_df = self.df[(self.df['grade'] >= bottom_margin) & (self.df['grade'] <= top_margin)].copy()

        filtered_df['efficiency'] = filtered_df['grade'] / filtered_df['time']

        top_5 = filtered_df.sort_values(by='efficiency', ascending=False).head(5)

        result = []
        for index, row in top_5.iterrows():
            result.append((row['id'], row['grade'], round(row['efficiency'], 2)))

        return tuple(result)


class Plots:
    def set_cat(self, catalog):
        self.catalog = catalog
        if not os.path.exists(catalog):
            os.makedirs(catalog)

    def avg_plot(self, avg_data, name_prefix=""):
        plt.figure(figsize=(8, 5))
        questions = [f"Q{i + 1}" for i in range(len(avg_data))]
        plt.bar(questions, avg_data, color='skyblue')
        plt.title(f"{name_prefix} Відсоток правильних відповідей")
        plt.ylabel("Відсоток успішності")
        plt.ylim(0, 100)

        filename = f"{self.catalog}/{name_prefix}_avg_plot.png"
        plt.savefig(filename)
        print(f"Графік збережено: {filename}")
        plt.close()

    def marks_plot(self, marks_data, name_prefix=""):
        plt.figure(figsize=(8, 5))
        grades = list(marks_data.keys())
        counts = list(marks_data.values())

        plt.bar(grades, counts, color='lightgreen', width=1.5)
        plt.title(f"{name_prefix} Розподіл оцінок")
        plt.xlabel("Оцінка")
        plt.ylabel("Кількість студентів")

        filename = f"{self.catalog}/{name_prefix}_marks_plot.png"
        plt.savefig(filename)
        print(f"Графік збережено: {filename}")
        plt.close()

    def best_marks_plot(self, best_data, name_prefix=""):
        if not best_data:
            return

        ids = [item[0] for item in best_data]
        effs = [item[2] for item in best_data]

        plt.figure(figsize=(8, 5))
        plt.bar(ids, effs, color='salmon')
        plt.title(f"{name_prefix} Топ-5 за ефективністю (бал/хв)")
        plt.ylabel("Балів за хвилину")
        plt.xticks(rotation=45)
        plt.tight_layout()

        filename = f"{self.catalog}/{name_prefix}_best_marks.png"
        plt.savefig(filename)
        print(f"Графік збережено: {filename}")
        plt.close()


class KmrWork(KmrCsv, Statistic, Plots):
    kmrs = {}
    cat = "plots_result"

    def __init__(self, csv_ref, kmr_num):
        self.set_ref(csv_ref)
        self.set_num(kmr_num)
        self.read_csv()
        self.set_cat(KmrWork.cat)

        KmrWork.kmrs[kmr_num] = csv_ref

    def compare_csv(self, other_kmr):
        lines = []
        lines.append(f"--- ПОРІВНЯННЯ КМР {self.num} та КМР {other_kmr.num}")

        count1 = len(self.df)
        count2 = len(other_kmr.df)
        lines.append(f"Кількість студентів: КМР{self.num}={count1}, КМР{other_kmr.num}={count2}")

        avg1 = self.df['grade'].mean()
        avg2 = other_kmr.df['grade'].mean()
        lines.append(f"Середній бал: КМР{self.num}={avg1:.2f}, КМР{other_kmr.num}={avg2:.2f}")

        time1 = self.df['time'].mean()
        time2 = other_kmr.df['time'].mean()
        lines.append(f"Середній час (хв): КМР{self.num}={time1:.2f}, КМР{other_kmr.num}={time2:.2f}")

        for line in lines:
            print(line)

        with open(f"{self.cat}/comparison_report.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print("Звіт збережено у comparison_report.txt")

    def compare_avg_plots(self, other_kmr):
        stat1 = self.avg_stat()
        stat2 = other_kmr.avg_stat()

        questions = [f"Q{i + 1}" for i in range(len(stat1))]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        ax1.bar(questions, stat1, color='blue', alpha=0.6)
        ax1.set_title(f"КМР {self.num}")
        ax1.set_ylim(0, 100)

        ax2.bar(questions, stat2, color='green', alpha=0.6)
        ax2.set_title(f"КМР {other_kmr.num}")
        ax2.set_ylim(0, 100)

        plt.suptitle("Порівняння успішності по питаннях")
        filename = f"{self.cat}/comparison_plots.png"
        plt.savefig(filename)
        print(f"Порівняльний графік збережено: {filename}")
        plt.close()


print("\n--- 1. СТВОРЕННЯ ОБ'ЄКТІВ")
kmr1 = KmrWork("kmr1.csv", 1)
kmr2 = KmrWork("kmr2.csv", 2)

kmr1.file_info()
kmr2.file_info()

print("\n--- 2. ГРАФІКИ ДЛЯ KMР2")

avg_data_2 = kmr2.avg_stat()
kmr2.avg_plot(avg_data_2, name_prefix="KMР2")

marks_data_2 = kmr2.marks_stat()
kmr2.marks_plot(marks_data_2, name_prefix="KMР2")

best_res = kmr2.best_marks_per_time(60, 100)
kmr2.best_marks_plot(best_res, name_prefix="KMР2")

print("\n--- 3.Порівняння")

kmr1.compare_csv(kmr2)
kmr1.compare_avg_plots(kmr2)