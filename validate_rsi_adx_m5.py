"""Validacao RSI+ADX M5 — 39 ativos universo oficial, sem lookahead."""
import pandas as pd, numpy as np, yfinance as yf

FOREX = ["EURUSD=X","GBPUSD=X","USDJPY=X","USDCHF=X","AUDUSD=X","NZDUSD=X","USDCAD=X",
"EURGBP=X","EURJPY=X","EURCHF=X","EURAUD=X","EURNZD=X","EURCAD=X","GBPCHF=X","GBPAUD=X",
"GBPNZD=X","GBPCAD=X","CHFJPY=X","AUDJPY=X","AUDCHF=X","AUDNZD=X","NZDJPY=X","NZDCHF=X",
"NZDCAD=X","CADJPY=X","CADCHF=X","USDAUD=X"]
CRYPTO = ["BTC-USD","ETH-USD","BNB-USD","XRP-USD","LTC-USD","SOL-USD","DOGE-USD","AVAX-USD","SUI-USD","XLM-USD","XPL-USD","LINK-USD"]
SYMBOLS = FOREX + CRYPTO

def compute(df):
    h, l, c = df["High"].astype(float), df["Low"].astype(float), df["Close"].astype(float)
    o = df["Open"].astype(float)
    # RSI Wilder 14
    d = c.diff()
    g = d.clip(lower=0); loss = -d.clip(upper=0)
    ag = g.ewm(alpha=1/14, adjust=False).mean()
    al = loss.ewm(alpha=1/14, adjust=False).mean()
    rs = ag / al.replace(0, np.nan)
    rsi = (100 - 100/(1+rs)).fillna(50.0)
    # ADX Wilder 14 + DI
    up = h.diff().clip(lower=0); dn = (-l.diff()).clip(lower=0)
    pm = pd.Series(np.where(up > dn, up, 0.0), index=df.index)
    mm = pd.Series(np.where(dn > up, dn, 0.0), index=df.index)
    tr = pd.concat([(h-l).abs(), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    atrw = tr.ewm(alpha=1/14, adjust=False).mean()
    pdi = 100*(pm.ewm(alpha=1/14, adjust=False).mean()/atrw.replace(0,np.nan))
    mdi = 100*(mm.ewm(alpha=1/14, adjust=False).mean()/atrw.replace(0,np.nan))
    dx = (100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan)).fillna(0.0)
    adx = dx.ewm(alpha=1/14, adjust=False).mean().fillna(0.0)
    return pd.DataFrame({"o":o,"c":c,"rsi":rsi.fillna(50.0),"adx":adx.fillna(0.0),
                         "pdi":pdi.fillna(0.0),"mdi":mdi.fillna(0.0)})

rows=[]
for s in SYMBOLS:
    try:
        df = yf.Ticker(s).history(period="5d", interval="5m", auto_adjust=False)
        if df is None or len(df) < 60:
            rows.append((s,0,0,0,0,0,0,"SEM_DADOS")); continue
        df = df.dropna(subset=["Open","High","Low","Close"])
        ind = compute(df)
        nb=wb=nf=wf=0
        for i in range(14, len(ind)-1):
            o,c = ind["o"].iloc[i], ind["c"].iloc[i]
            if c==o: continue
            d = "BUY" if c>o else "SELL"
            o2,c2 = ind["o"].iloc[i+1], ind["c"].iloc[i+1]
            if c2==o2: continue
            hit = (d=="BUY" and c2>o2) or (d=="SELL" and c2<o2)
            nb+=1; wb+=hit
            rsi,adx,pdi,mdi = ind["rsi"].iloc[i],ind["adx"].iloc[i],ind["pdi"].iloc[i],ind["mdi"].iloc[i]
            ok = False
            if d=="BUY": ok = (adx>=20) and (pdi>mdi) and (50<=rsi<=70)
            else: ok = (adx>=20) and (mdi>pdi) and (30<=rsi<=50)
            if ok: nf+=1; wf+=hit
        ab = round(100*wb/nb,2) if nb else 0; af = round(100*wf/nf,2) if nf else 0
        rows.append((s,nb,wb,ab,nf,wf,af,"OK"))
    except Exception as e:
        rows.append((s,0,0,0,0,0,0,f"ERRO {e}"))
r=pd.DataFrame(rows, columns=["symbol","n_base","wins_base","acc_base","n_filt","wins_filt","acc_filt","st"])
r["delta_pp"]=round(r["acc_filt"]-r["acc_base"],2)
r["cobertura"]=np.where(r["n_base"]>0, (r["n_filt"]/r["n_base"]).round(3), 0.0)
r["fp_cut"]=np.where(r["n_base"]>0, round(100*(1-r["n_filt"]/r["n_base"]),1), 0.0)
print(r.to_string(index=False))
print("\n--- AGREGADO ---")
tb, wb = int(r["n_base"].sum()), int(r["wins_base"].sum())
tf, wf = int(r["n_filt"].sum()), int(r["wins_filt"].sum())
print(f"BASE: {wb}/{tb} = {100*wb/tb:.2f}% | FILT: {wf}/{tf} = {100*wf/tf:.2f}% | delta {100*wf/tf-100*wb/tb:+.2f}pp | sinais -{100*(1-tf/tb):.1f}%")
elig = r[(r.st=="OK")&(r.n_filt>=10)].sort_values(["acc_filt","n_filt"], ascending=[False,False]).head(3)
print("\n--- TOP3 (n_filt>=10) ---")
print(elig[["symbol","n_base","acc_base","n_filt","acc_filt","delta_pp","fp_cut"]].to_string(index=False))
r.to_csv("rsi_adx_m5_result.csv", index=False)
