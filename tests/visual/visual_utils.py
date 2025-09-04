import os
from PIL import Image, ImageChops

BASELINE_DIR = "./tests/visual/visual_baselines"
RESULTS_DIR = "./tests/visual/visual_results"
DIFFS_DIR = "./tests/visual/visual_diffs"

os.makedirs(BASELINE_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(DIFFS_DIR, exist_ok=True)

def assert_screenshot(driver, name, threshold=0):
    """
    Сравнивает текущий скриншот с baseline.
    Если baseline нет — создаёт его.
    Если есть — сравнивает и при расхождении сохраняет diff.
    threshold = допустимый порог отличий (0 = строгое сравнение).
    """
    baseline_path = os.path.join(BASELINE_DIR, name)
    result_path = os.path.join(RESULTS_DIR, name)
    diff_path = os.path.join(DIFFS_DIR, name)

    # Сохраняем новый скрин
    driver.save_screenshot(result_path)

    if not os.path.exists(baseline_path):
        os.replace(result_path, baseline_path)  # первый запуск → baseline
        return

    baseline = Image.open(baseline_path).convert("RGB")
    result = Image.open(result_path).convert("RGB")

    # Сравнение
    diff = ImageChops.difference(baseline, result)

    # diff.getbbox() вернёт None, если картинка идентична
    if diff.getbbox() is None:
        return

    # Подсчёт "силы" отличий
    diff_hist = diff.histogram()
    sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(diff_hist))
    sum_of_squares = sum(sq)
    rms = (sum_of_squares / float(baseline.size[0] * baseline.size[1])) ** 0.5

    if rms <= threshold:
        return  # различия в пределах допустимого

    diff.save(diff_path)
    raise AssertionError(f"Visual diff found. See {diff_path}")
