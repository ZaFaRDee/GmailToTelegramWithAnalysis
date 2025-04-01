# fundamental_analysis.py

import yfinance as yf

def shorten_number(n):
    try:
        n = float(n)
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

def get_fundamental_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info

    metrics = {
        "Market Cap": info.get("marketCap", "?"),
        "Income": info.get("netIncomeToCommon", "?"),
        "P/E": info.get("trailingPE", "?"),
        "PEG": info.get("pegRatio", "?"),
        "P/S": info.get("priceToSalesTrailing12Months", "?"),
        "P/B": info.get("priceToBook", "?"),
        "EPS": info.get("trailingEps", "?"),
        "Insider Ownership (%)": info.get("heldPercentInsiders", "?"),
        "Institutional Ownership (%)": info.get("heldPercentInstitutions", "?"),
        "Short Interest (%)": info.get("shortPercentOfFloat", "?"),
        "Avg Volume": info.get("averageVolume", "?"),
        "Call Volume": "?",
        "Put Volume": "?"
    }

    # Call/Put Volume
    try:
        chain = stock.option_chain()
        metrics["Call Volume"] = int(chain.calls['volume'].sum())
        metrics["Put Volume"] = int(chain.puts['volume'].sum())
    except:
        pass

    good = 0
    total = 0
    evals = {}

    for key, value in metrics.items():
        if value == "?":
            evals[key] = f"❓ <b>{key}:</b> ?"
            continue

        try:
            val = float(value)
            is_good = False

            if key == "Market Cap":
                is_good = val > 1_000_000_000
            elif key == "Income":
                is_good = val > 0
            elif key == "P/E":
                is_good = 5 < val < 25
            elif key == "PEG":
                is_good = 0 < val < 1.5
            elif key == "P/S":
                is_good = val < 4
            elif key == "P/B":
                is_good = val < 3
            elif key == "EPS":
                is_good = val > 0
            elif key == "Insider Ownership (%)":
                is_good = val > 0.01
            elif key == "Institutional Ownership (%)":
                is_good = val > 0.3
            elif key == "Short Interest (%)":
                is_good = val < 0.15
            elif key == "Avg Volume":
                is_good = val > 100_000
            elif key == "Call Volume":
                is_good = val > 100
            elif key == "Put Volume":
                is_good = val > 100

            mark = "🟢" if is_good else "🔴"
            if is_good:
                good += 1
            total += 1

            # Format
            display_val = f"{val:.2f}" if key in ["P/E", "PEG", "P/S", "P/B", "EPS"] else shorten_number(val)
            evals[key] = f"{mark} <b>{key}:</b> {display_val}"

        except Exception:
            evals[key] = f"❓ <b>{key}:</b> ?"

    summary = f"📊 <b>Fundamental:</b> {good}/{total}"
    return evals, summary
