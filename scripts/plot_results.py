"""
Visualise acoustic index separation between biophony (B) and anthropophony (A).

Produces a three-panel figure:
  1. PCA scatter (PC1 vs PC2) with 95% confidence ellipses
  2. PC1 loading bar chart — which indices drive the separation
  3. Scree plot — cumulative variance explained

Output: ../figures/pca_results.png
"""

import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

SCORES_CSV = os.path.join(os.path.dirname(__file__), '..', 'scores.csv')
FIGURES_DIR = os.path.join(os.path.dirname(__file__), '..', 'figures')

FEATURE_COLS = [
    'median', 'tH', 'tActivity', 'ACI', 'fH', 'H_of_avg_spectrum',
    'Kurt_spectral_max', 'Skew_spectral_max', 'LFC', 'MFC', 'HFC',
    'soundscape_index', 'Leq', 'LeqF_from_spectrogram', 'AGI',
    'bw50', 'bw90', 'tS2N', 'sS2N',
]

COLORS = {'A': '#D95F4B', 'B': '#3A7DC9'}
LABELS = {'A': 'Anthropophony', 'B': 'Biophony'}
FONT = {'family': 'sans-serif'}


def confidence_ellipse(x, y, ax, n_std=2.0, **kwargs):
    if len(x) < 3:
        return
    cov = np.cov(x, y)
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals, vecs = vals[order], vecs[:, order]
    angle = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * n_std * np.sqrt(vals)
    ax.add_patch(Ellipse(
        xy=(np.mean(x), np.mean(y)),
        width=width, height=height, angle=angle, **kwargs
    ))


def despine(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def main():
    df = pd.read_csv(SCORES_CSV)
    df = df.dropna(subset=FEATURE_COLS)

    X = df[FEATURE_COLS].values
    groups = df['group'].values

    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA(n_components=min(len(FEATURE_COLS), len(df)))
    X_pca = pca.fit_transform(X_scaled)
    explained = pca.explained_variance_ratio_ * 100
    loadings = pca.components_.T  # (n_features, n_components)

    os.makedirs(FIGURES_DIR, exist_ok=True)

    plt.rcParams.update({
        'font.size': 11,
        'axes.titlesize': 12,
        'axes.titleweight': 'bold',
        'axes.labelsize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
    })

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.suptitle('Acoustic Index PCA — Biophony vs Anthropophony',
                 fontsize=14, fontweight='bold', y=1.02)

    # --- Panel 1: PCA scatter ---
    ax = axes[0]
    for grp in ('A', 'B'):
        mask = groups == grp
        ax.scatter(
            X_pca[mask, 0], X_pca[mask, 1],
            c=COLORS[grp], label=LABELS[grp],
            alpha=0.70, edgecolors='white', linewidths=0.5, s=55, zorder=3
        )
        confidence_ellipse(
            X_pca[mask, 0], X_pca[mask, 1], ax,
            n_std=2.0, edgecolor=COLORS[grp], facecolor=COLORS[grp],
            alpha=0.13, linewidth=2.0, zorder=2
        )

    ax.axhline(0, color='#AAAAAA', linewidth=0.7, linestyle='--', zorder=1)
    ax.axvline(0, color='#AAAAAA', linewidth=0.7, linestyle='--', zorder=1)
    ax.set_xlabel(f'PC1 ({explained[0]:.1f}% variance)')
    ax.set_ylabel(f'PC2 ({explained[1]:.1f}% variance)')
    ax.set_title('PCA Scatter')
    ax.legend(frameon=False)
    despine(ax)

    # --- Panel 2: PC1 loading bar chart (sorted) ---
    ax = axes[1]

    pc1_loadings = loadings[:, 0]
    order = np.argsort(pc1_loadings)
    sorted_feats = [FEATURE_COLS[i] for i in order]
    sorted_vals = pc1_loadings[order]
    bar_colors = [COLORS['A'] if v > 0 else COLORS['B'] for v in sorted_vals]

    ax.barh(sorted_feats, sorted_vals, color=bar_colors, edgecolor='white',
            height=0.65, zorder=3)
    ax.axvline(0, color='#333333', linewidth=0.9, zorder=4)
    ax.xaxis.grid(True, color='#EEEEEE', linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel(f'PC1 Loading  ({explained[0]:.1f}% variance)')
    ax.set_title('Feature Loadings on PC1')
    ax.tick_params(axis='y', labelsize=8.5)

    legend_handles = [
        mpatches.Patch(color=COLORS['A'], label=f'{LABELS["A"]} →'),
        mpatches.Patch(color=COLORS['B'], label=f'← {LABELS["B"]}'),
    ]
    ax.legend(handles=legend_handles, frameon=False)
    despine(ax)
    ax.spines['left'].set_visible(False)

    # --- Panel 3: Scree plot ---
    ax = axes[2]
    n_show = min(10, len(explained))
    cumulative = np.cumsum(explained[:n_show])
    x = np.arange(1, n_show + 1)

    ax.bar(x, explained[:n_show], color='#6BAED6', edgecolor='white',
           label='Per-component', zorder=3)
    ax.plot(x, cumulative, 'o-', color=COLORS['A'], linewidth=2.0,
            markersize=6, markeredgecolor='white', markeredgewidth=0.8,
            label='Cumulative', zorder=4)
    ax.axhline(80, color='#AAAAAA', linewidth=0.9, linestyle='--')
    ax.text(n_show - 0.1, 81.5, '80%', fontsize=8, color='#888888',
            va='bottom', ha='right')
    ax.yaxis.grid(True, color='#EEEEEE', linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel('Principal Component')
    ax.set_ylabel('Variance Explained (%)')
    ax.set_title('Scree Plot')
    ax.set_xticks(x)
    ax.set_ylim(0, 105)
    ax.legend(frameon=False)
    despine(ax)

    plt.tight_layout(pad=1.8)
    out_path = os.path.join(FIGURES_DIR, 'pca_results.png')
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    print(f'Saved: {out_path}')


if __name__ == '__main__':
    main()
