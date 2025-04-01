from finvizfinance.quote import finvizfinance
from finviz_wrapper import get_finviz_data


def shorten_number(n):
    try:
        n = float(str(n).replace('%', '').replace('B', 'e9').replace('M', 'e6').replace('K', 'e3'))
        abs_n = abs(n)
        if abs_n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.1f}B"
        elif abs_n >= 1_000_000:
            return f"{n / 1_000_000:.1f}M"
        elif abs_n >= 1_000:
            return f"{n / 1_000:.1f}k"
        else:
            return f"{n:.0f}"
    except:
        return "?"

def get_finviz_analysis(ticker):
    try:
        stock = finvizfinance(ticker)
        data = get_finviz_data(ticker)
    except Exception as e:
        return {}, f"📊 Fundamental (Finviz): ?/14\n⚠️ Ma'lumot yuklashda xatolik: {e}"

    fields = {
        "Market Cap": lambda v: "B" in v or "M" in v,
        "P/E": lambda v: 5 < float(v) < 25,
        "PEG": lambda v: 0 < float(v) < 1.5,
        "P/S": lambda v: float(v) < 4,
        "P/B": lambda v: float(v) < 3,
        "EPS (ttm)": lambda v: float(v) > 0,
        "Insider Own": lambda v: float(v.strip('%')) > 1,
        "Inst Own": lambda v: float(v.strip('%')) > 30,
        "ROA": lambda v: float(v.strip('%')) > 0,
        "ROE": lambda v: float(v.strip('%')) > 0,
        "Debt/Eq": lambda v: float(v) < 1,
        "Current Ratio": lambda v: float(v) >= 1,
        "Short Float": lambda v: float(v.strip('%')) < 15,
        "Target Price": lambda v: float(v) > 0,
    }

    good, total = 0, 0
    evals = {}

    for key, rule in fields.items():
        value = data.get(key, "?")
        if value == "-" or value == "":
            value = "?"
        if value == "?":
            evals[key] = f"❓ <b>{key}:</b> ?"
            continue
        try:
            if rule(value):
                mark = "🟢"
                good += 1
            else:
                mark = "🔴"
            formatted = value if "%" in value or any(x in value for x in "MB") else shorten_number(value)
            evals[key] = f"{mark} <b>{key}:</b> {formatted}"
            total += 1
        except:
            evals[key] = f"❓ <b>{key}:</b> ?"

    summary = f"📊 Fundamental (Finviz): {good}/{total}"
    return evals, summary