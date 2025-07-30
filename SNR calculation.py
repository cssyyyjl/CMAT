import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


base_path = Path()


F = np.load()          # (n_cells, n_timepoints)
Fneu = np.load()    # (n_cells, n_timepoints)
iscell = np.load()[:, 0].astype(bool)


r = 0.7
Fcorr = F - r * Fneu
Fcorr_cells = Fcorr[iscell]

def compute_dff(f, detrend_window=100, baseline_percentile=25, epsilon=1e-7):

    f0 = np.percentile(f, baseline_percentile, axis=1, keepdims=True)
    f0 = np.clip(f0, epsilon, None)
    return (f - f0) / f0


dFF = compute_dff(Fcorr_cells, detrend_window=100, baseline_percentile=25, epsilon=1e-7)

def compute_snr(dff, top_percent=10, epsilon=1e-10):

    snrs = []
    for trace in dff:
        sorted_trace = np.sort(trace)
        n = len(sorted_trace)
        n_top = max(1, int(n * top_percent / 100))
        signal = np.mean(sorted_trace[-n_top:])
        n_noise = n - n_top
        noise = np.std(sorted_trace[:n_noise]) if n_noise > 0 else epsilon
        noise = max(noise, epsilon)
        snr = signal / noise
        snrs.append(snr)
    return np.array(snrs)


snrs_mean = compute_snr(dFF, top_percent=10, epsilon=1e-10)


mask = (snrs_mean > 3) & (snrs_mean < 11)
filtered_snrs = snrs_mean[mask]
filtered_cell_ids = np.where(iscell)[0][mask]

print({len(snrs_mean)} )
print({len(filtered_snrs)}, len(filtered_snrs)/len(snrs_mean))

# 保存筛选后的结果
df = pd.DataFrame({
    "Cell_ID": filtered_cell_ids,
    "SNR_mean": filtered_snrs
})
save_path =
df.to_excel(save_path, index=False, engine='openpyxl')
print({save_path})


mean_snr = np.mean(filtered_snrs)
std_snr = np.std(filtered_snrs)
median_snr = np.median(filtered_snrs)

print(f"\n[seleted cells]\nMean SNR = {mean_snr:.2f} ± {std_snr:.2f} (SD)")
print(f"Median SNR = {median_snr:.2f}")
print(f"Total Cells = {len(filtered_snrs)}")


plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(filtered_snrs, bins=20, color='skyblue', edgecolor='black', alpha=0.7)


stats_text = (f'Mean = {mean_snr:.2f}\n'
              f'Std = {std_snr:.2f}\n'
              f'Median = {median_snr:.2f}\n'
              f'n = {len(filtered_snrs)}')
plt.text(0.95, 0.95, stats_text,
         transform=plt.gca().transAxes,
         verticalalignment='top',
         horizontalalignment='right',
         bbox=dict(facecolor='white', alpha=0.8),
         fontsize=10)

plt.xlabel('SNR (filtered <10)', fontsize=12)
plt.ylabel('Number of Cells', fontsize=12)
plt.title('Distribution of SNR Values (SNR < 10)', fontsize=14)
plt.tight_layout()
plt.show()