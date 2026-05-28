import difflib
import re


def normalize_text(phrase):
    """
    Удаляет пунктуацию, приводит к нижнему регистру, удаляет лишние пробелы
    """
    phrase = phrase.lower()
    phrase = re.sub(r'[^a-zа-я0-9\s]', ' ', phrase)  # убрать всё, кроме букв и цифр
    phrase = re.sub(r'\s+', ' ', phrase).strip()
    return phrase


def extra_normalize_text(phrase):
    """
    Удаляет пунктуацию, приводит к нижнему регистру, удаляет лишние пробелы
    """
    phrase = phrase.lower()
    phrase = re.sub(r'[^a-zа-я\s]', ' ', phrase)  # убрать всё, кроме букв и цифр
    phrase = re.sub(r'\s+', ' ', phrase).strip()
    return phrase

def bidirectional_similarity(words1, words2):
    def max_sim_average(source, target):
        total = 0.0
        for w1 in source:
            scores = [difflib.SequenceMatcher(None, w1, w2).ratio() for w2 in target]
            total += max(scores) if scores else 0
        return total / len(source) if source else 0

    s1 = max_sim_average(words1, words2)
    s2 = max_sim_average(words2, words1)
    return (s1 + s2) / 2  # усредняем

def windowed_similarity(long_words, short_words):
    max_score = 0.0
    short_len = len(short_words)
    for window_size in range(short_len, short_len + 2):
        for i in range(len(long_words) - window_size + 1):
            window = long_words[i:i + window_size]
            score = bidirectional_similarity(window, short_words)
            if score > max_score:
                max_score = score
    return max_score


def compare_phrases(p1, p2):
    w1 = normalize_text(p1).split()
    w2 = normalize_text(p2).split()

    if len(w1) > len(w2) + 1:
        return windowed_similarity(w1, w2)
    elif len(w2) > len(w1) + 1:
        return windowed_similarity(w2, w1)
    else:
        return bidirectional_similarity(w1, w2)


def extra_compare_phrases(p1, p2):
    w1 = extra_normalize_text(p1).split()
    w2 = extra_normalize_text(p2).split()

    if len(w1) > len(w2) + 1:
        return windowed_similarity(w1, w2)
    elif len(w2) > len(w1) + 1:
        return windowed_similarity(w2, w1)
    else:
        return bidirectional_similarity(w1, w2)


def filter_matches(matches, threshold=0.15):
    # Сортируем по второму элементу кортежа (по убыванию)
    matches.sort(key=lambda x: x[1], reverse=True)

    filtered = []
    for i, match in enumerate(matches):
        if i == 0:
            filtered.append(match)
        else:
            if filtered[0][1] - match[1] <= threshold:
                filtered.append(match)
            else:
                break  # Прерываем, как только разница превысила threshold
    return filtered


def match_phrases(array1, array2, threshold=0.5):
    # Словарь: ключ - фраза из array1, значение - список (phrase2, score)
    matches_dict = {phrase1: [] for phrase1 in array1}
    matched_in_2 = set()

    for phrase1 in array1:
        for phrase2 in array2:
            score = compare_phrases(phrase1, phrase2)
            if score >= threshold:
                matches_dict[phrase1].append((phrase2, score))
                matched_in_2.add(phrase2)

    results = []
    # Формируем результат по array1
    for phrase1, matches in matches_dict.items():
        if matches:
            # сортируем по убыванию оценки
            matches.sort(key=lambda x: x[1], reverse=True)
            matches = filter_matches(matches)
            matched_phrases = [m[0] for m in matches]
            max_score = matches[0][1]
            arr_score = [m[1] for m in matches]
            results.append((phrase1, matched_phrases, arr_score))
        else:
            max_match_score = 0.0
            max_match_phrase = '---'
            for phrase2 in array2:
                score = extra_compare_phrases(phrase1, phrase2)
                if score >= threshold:
                    if score > max_match_score:
                        max_match_score = score
                        max_match_phrase = phrase2
            results.append((phrase1, [max_match_phrase], [max_match_score]))

    # Добавляем фразы из второго массива без пары
    for phrase2 in array2:
        if phrase2 not in matched_in_2:
            results.append((None, [phrase2], [0.0]))

    return results





