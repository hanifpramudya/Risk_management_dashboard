import pandas as pd
import numpy as np

def initialize_fixed_data():
    """Initialize fixed data for the dashboard instead of using random/dummy data"""

    # Create fixed Data_YTD structure
    parameters = [
        'Parameter', 'Aset Investasi', 'Deposito Berjangka', 'Obligasi Korporasi',
        'Surat Berharga yang Diterbitkan oleh Negara RI', 'Reksa Dana', 'Kas dan Bank',
        'Piutang Premi', 'Piutang Reasuransi', 'Piutang Lain-lain', 'Jumlah Aset',
        'Liabilitas Reasuransi', 'Hutang Klaim', 'Hutang Komisi', 'Hutang Lain-lain',
        'Jumlah Utang', 'Jumlah Ekuitas', 'Premi Bruto (All)', 'Premi Bruto (Life)',
        'Premi Bruto (Non-Life)', 'Premi Bruto (Health)', 'Premi Reasuransi (All)',
        'Premi Reasuransi (Life)', 'Premi Reasuransi (Non-Life)', 'Premi Reasuransi (Health)',
        'Jumlah Pendapatan', 'Klaim Bruto (All)', 'Klaim Bruto (Life)', 'Klaim Bruto (Non-Life)',
        'Klaim Bruto (Health)', 'Klaim Reasuransi (All)', 'Klaim Reasuransi (Life)',
        'Klaim Reasuransi (Non-Life)', 'Klaim Reasuransi (Health)', 'Beban Komisi (All)',
        'Beban Komisi (Life)', 'Beban Komisi (Non-Life)', 'Beban Komisi (Health)',
        'Beban Operasional', 'Beban Underwriting Lain', 'Pendapatan Investasi', 'Beban Investasi',
        'Laba (Rugi) Underwriting', 'Total Laba (Rugi) Komprehensif', 'Laba (Rugi) Lainnya',
        'Modal Saham', 'Agio Saham', 'Cadangan Umum', 'Laba (Rugi) Belum Direalisasi',
        'Saldo Laba', 'Rasio Solvabilitas', 'RBC', 'Likuiditas', 'Rasio Beban Operasional',
        'Rasio Beban Klaim', 'Loss Ratio (All)', 'Loss Ratio (Life)', 'Loss Ratio (Non-Life)',
        'Loss Ratio (Health)', 'Expense Ratio (All)', 'Expense Ratio (Life)',
        'Expense Ratio (Non-Life)', 'Expense Ratio (Health)', 'Combined Ratio (All)',
        'Combined Ratio (Life)', 'Combined Ratio (Non-Life)', 'Combined Ratio (Health)',
        'ROA', 'ROE', 'NPM', 'Debt to Equity Ratio', 'Asset Turnover', 'Equity Multiplier',
        'Investment Return', 'Premium Growth Rate', 'Claim Growth Rate', 'Operating Expense Growth Rate',
        'Retention Ratio (All)', 'Retention Ratio (Life)', 'Retention Ratio (Non-Life)',
        'Retention Ratio (Health)', 'Reinsurance Ratio (All)', 'Reinsurance Ratio (Life)',
        'Reinsurance Ratio (Non-Life)', 'Reinsurance Ratio (Health)', 'Premium to Surplus Ratio',
        'Reserve to Premium Ratio', 'Investment Yield', 'Cash Flow from Operations',
        'Cash Flow from Investments', 'Cash Flow from Financing', 'Net Cash Flow',
        'Receivables Turnover', 'Days Sales Outstanding', 'Payables Turnover',
        'Days Payable Outstanding', 'Working Capital', 'Current Ratio', 'Quick Ratio',
        'Asset Quality Ratio', 'Non-Performing Assets Ratio', 'Capital Adequacy Ratio',
        'Tier 1 Capital Ratio', 'Tier 2 Capital Ratio', 'Leverage Ratio', 'Jumlah Karyawan',
        'Jumlah Agen', 'Jumlah Kantor Cabang', 'Jumlah Produk', 'Market Share (Life)',
        'Market Share (Non-Life)', 'Market Share (Health)', 'Customer Satisfaction Index',
        'Net Promoter Score', 'Employee Satisfaction Index', 'Training Hours per Employee',
        'IT Investment Ratio', 'Digital Channel Usage', 'Mobile App Downloads', 'Online Premium Ratio',
        'Jumlah Polis', 'Jumlah Fraud', 'Jumlah Komplain', 'Komplain Resolution Rate',
        'Average Claim Settlement Days', 'Underwriting Profit Margin', 'Investment Portfolio Diversity',
        'Alternative Investment Ratio', 'Real Estate Investment Ratio', 'Equity Investment Ratio',
        'Fixed Income Investment Ratio', 'Government Bond Ratio', 'Corporate Bond Ratio',
        'Jumlah Gugatan', 'Jumlah Nominal Gugatan Yang Sedang Diajukan', 'Jumlah Pelanggaran Atas Ketentuan',
        'Jumlah Pelanggaran Atas Ketentuan Yang Belum Diselesaikan',
        'Jumlah Pelanggaran Atas Ketentuan Yang Sudah Diselesaikan', 'Jumlah Denda',
        'Jumlah Denda Yang Belum Dibayar', 'Jumlah Pengaduan', 'Jumlah Pengaduan Yang Belum Ditindak Lanjuti',
        'Indak Lanjut Pengaduan', 'Jumlah Pemberitaan Negatif', 'Jumlah Pemberitaan Negatif Dalam 1 Tahun'
    ]

    # Fixed values for 12 months (based on dashboard requirements)
    # Index mapping from dashboard.py:
    # 0: Aset Investasi
    # 1: Deposito Berjangka
    # 2: Obligasi Korporasi
    # 3: Surat Berharga yang Diterbitkan oleh Negara RI
    # 4: Reksa Dana
    # 5: Kas dan Bank
    # 9: Jumlah Aset
    # 14: Jumlah Utang
    # 15: Jumlah Ekuitas
    # 16: Premi Bruto (All)
    # 25: Jumlah Pendapatan
    # 26: Klaim Bruto (All)
    # 43: Total Laba (Rugi) Komprehensif
    # 51: RBC
    # 116: Jumlah Polis
    # 117: Jumlah Fraud
    # 132: Jumlah Gugatan
    # 133: Jumlah Nominal Gugatan Yang Sedang Diajukan
    # 134: Jumlah Pelanggaran Atas Ketentuan
    # 137: Jumlah Denda
    # 139: Jumlah Pengaduan
    # 141: Indak Lanjut Pengaduan
    # 143: Jumlah Pemberitaan Negatif Dalam 1 Tahun

    months = ['Aug-2024', 'Sep-2024', 'Oct-2024', 'Nov-2024', 'Dec-2024',
              'Jan-2025', 'Feb-2025', 'Mar-2025', 'Apr-2025', 'May-2025',
              'Jun-2025', 'Jul-2025', 'Aug-2025']

    # Fixed financial data for each month (12 months progression)
    fixed_monthly_data = {
        0: [3200.50, 3250.75, 3300.25, 3350.80, 3400.50, 3450.25, 3500.00, 3550.75, 3600.50, 3650.25, 3700.00, 3750.50, 3800.75],  # Aset Investasi
        1: [1500.00, 1520.00, 1540.00, 1560.00, 1580.00, 1600.00, 1620.00, 1640.00, 1660.00, 1680.00, 1700.00, 1720.00, 1740.00],  # Deposito Berjangka
        2: [850.00, 860.00, 870.00, 880.00, 890.00, 900.00, 910.00, 920.00, 930.00, 940.00, 950.00, 960.00, 970.00],  # Obligasi Korporasi
        3: [600.00, 610.00, 620.00, 630.00, 640.00, 650.00, 660.00, 670.00, 680.00, 690.00, 700.00, 710.00, 720.00],  # Surat Berharga Negara RI
        4: [250.50, 260.75, 270.25, 280.80, 290.50, 300.25, 310.00, 320.75, 330.50, 340.25, 350.00, 360.50, 370.75],  # Reksa Dana
        5: [450.00, 465.00, 480.00, 495.00, 510.00, 525.00, 540.00, 555.00, 570.00, 585.00, 600.00, 615.00, 630.00],  # Kas dan Bank
        9: [8500.00, 8600.00, 8700.00, 8800.00, 8900.00, 9000.00, 9100.00, 9200.00, 9300.00, 9400.00, 9500.00, 9600.00, 9700.00],  # Jumlah Aset
        14: [3200.00, 3250.00, 3300.00, 3350.00, 3400.00, 3450.00, 3500.00, 3550.00, 3600.00, 3650.00, 3700.00, 3750.00, 3800.00],  # Jumlah Utang
        15: [5300.00, 5350.00, 5400.00, 5450.00, 5500.00, 5550.00, 5600.00, 5650.00, 5700.00, 5750.00, 5800.00, 5850.00, 5900.00],  # Jumlah Ekuitas
        16: [650.00, 670.00, 690.00, 710.00, 730.00, 750.00, 770.00, 790.00, 810.00, 830.00, 850.00, 870.00, 890.00],  # Premi Bruto (All)
        25: [720.00, 740.00, 760.00, 780.00, 800.00, 820.00, 840.00, 860.00, 880.00, 900.00, 920.00, 940.00, 960.00],  # Jumlah Pendapatan
        26: [380.00, 390.00, 400.00, 410.00, 420.00, 430.00, 440.00, 450.00, 460.00, 470.00, 480.00, 490.00, 500.00],  # Klaim Bruto (All)
        43: [185.00, 190.00, 195.00, 200.00, 205.00, 210.00, 215.00, 220.00, 225.00, 230.00, 235.00, 240.00, 245.00],  # Total Laba Rugi Komprehensif
        51: [165.50, 167.25, 169.00, 170.75, 172.50, 174.25, 176.00, 177.75, 179.50, 181.25, 183.00, 184.75, 186.50],  # RBC
        116: [45000, 45500, 46000, 46500, 47000, 47500, 48000, 48500, 49000, 49500, 50000, 50500, 51000],  # Jumlah Polis
        117: [2, 1, 3, 2, 1, 2, 1, 0, 2, 1, 1, 2, 1],  # Jumlah Fraud
        132: [5, 4, 6, 5, 4, 5, 3, 4, 5, 4, 3, 4, 5],  # Jumlah Gugatan
        133: [150.00, 140.00, 160.00, 155.00, 145.00, 150.00, 135.00, 140.00, 150.00, 145.00, 135.00, 140.00, 150.00],  # Nominal Gugatan
        134: [3, 2, 4, 3, 2, 3, 2, 1, 3, 2, 2, 3, 2],  # Jumlah Pelanggaran
        137: [25.00, 20.00, 30.00, 25.00, 20.00, 25.00, 15.00, 20.00, 25.00, 20.00, 15.00, 20.00, 25.00],  # Jumlah Denda
        139: [18, 15, 20, 17, 14, 16, 13, 15, 17, 14, 12, 15, 16],  # Jumlah Pengaduan
        141: [16, 14, 18, 16, 13, 15, 12, 14, 16, 13, 11, 14, 15],  # Tindak Lanjut Pengaduan
        143: [8, 7, 9, 8, 7, 8, 6, 7, 8, 7, 6, 7, 8],  # Pemberitaan Negatif
    }

    # Create YTD DataFrame
    ytd_data = {'Unnamed: 0': ['No'] + list(range(1, len(parameters))),
                'Parameter': parameters}

    # Add data for each month
    for month_idx, month in enumerate(months):
        month_name = month.split('-')[0]
        year = int(month.split('-')[1])

        # Year column
        ytd_data[month] = [year] + [np.nan] * (len(parameters) - 1)

        # Data column
        data_values = [month_name]  # First row is month name

        for param_idx in range(1, len(parameters)):
            if param_idx in fixed_monthly_data:
                # Use fixed data from mapping
                data_values.append(fixed_monthly_data[param_idx][month_idx])
            else:
                # Default values for other parameters
                if param_idx <= 50:
                    data_values.append(100.00 + param_idx * 10)
                elif param_idx <= 100:
                    data_values.append(1.50 + (param_idx % 10) * 0.5)
                else:
                    data_values.append(10 + param_idx % 20)

        ytd_data[f'Unnamed: {2 + month_idx * 2 + 1}'] = data_values

    df_ytd = pd.DataFrame(ytd_data)

    # Create Summary DataFrame with fixed risk scores
    risk_categories = [
        'Risiko Strategis',
        'Risiko Operasional',
        'Risiko Pasar',
        'Risiko Kredit',
        'Risiko Likuiditas',
        'Risiko Hukum',
        'Risiko Reputasi',
        'Risiko Teknologi Informasi',
        'Risiko Underwriting',
        '',
        'Composite Score',
    ]

    # Fixed risk scores for each category across months
    fixed_risk_scores = {
        'Risiko Strategis': [2.80, 2.75, 2.70, 2.65, 2.60, 2.55, 2.50, 2.45, 2.40, 2.35, 2.30, 2.25, 2.20],
        'Risiko Operasional': [3.20, 3.15, 3.10, 3.05, 3.00, 2.95, 2.90, 2.85, 2.80, 2.75, 2.70, 2.65, 2.60],
        'Risiko Pasar': [2.60, 2.65, 2.70, 2.75, 2.80, 2.85, 2.90, 2.85, 2.80, 2.75, 2.70, 2.65, 2.60],
        'Risiko Kredit': [2.40, 2.38, 2.36, 2.34, 2.32, 2.30, 2.28, 2.26, 2.24, 2.22, 2.20, 2.18, 2.16],
        'Risiko Likuiditas': [2.10, 2.08, 2.06, 2.04, 2.02, 2.00, 1.98, 1.96, 1.94, 1.92, 1.90, 1.88, 1.86],
        'Risiko Hukum': [2.90, 2.88, 2.86, 2.84, 2.82, 2.80, 2.78, 2.76, 2.74, 2.72, 2.70, 2.68, 2.66],
        'Risiko Reputasi': [2.50, 2.48, 2.46, 2.44, 2.42, 2.40, 2.38, 2.36, 2.34, 2.32, 2.30, 2.28, 2.26],
        'Risiko Teknologi Informasi': [3.00, 2.98, 2.96, 2.94, 2.92, 2.90, 2.88, 2.86, 2.84, 2.82, 2.80, 2.78, 2.76],
        'Risiko Underwriting': [2.70, 2.68, 2.66, 2.64, 2.62, 2.60, 2.58, 2.56, 2.54, 2.52, 2.50, 2.48, 2.46],
    }

    summary_data = {
        'Unnamed: 0': [''] * len(risk_categories),
        'Jenis Risiko': risk_categories
    }

    for month_idx, month in enumerate(months):
        month_name = month.split('-')[0]
        year = int(month.split('-')[1])
        full_month = {'Aug': 'August', 'Sep': 'September', 'Oct': 'October', 'Nov': 'November',
                      'Dec': 'December', 'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
                      'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July'}[month_name]

        scores = []
        for cat in risk_categories:
            if cat == '':
                scores.append('-')
            elif cat == 'Composite Score':
                # Calculate composite score as average of all risk scores
                avg_score = sum([s for s in scores if s != '-']) / len([s for s in scores if s != '-'])
                scores.append(round(avg_score, 2))
            else:
                scores.append(fixed_risk_scores[cat][month_idx])

        summary_data[f'{full_month}-{year}'] = [year] * len(risk_categories)
        summary_data[f'{full_month}-score'] = scores
        summary_data[f'{full_month}-weighted'] = [s if s == '-' else round(s * 0.8, 2) for s in scores]
        summary_data[f'{full_month}-classification'] = [
            '-' if s == '-' else ('High' if s > 3.5 else 'Moderate' if s > 2.5 else 'Low')
            for s in scores
        ]

    df_summary = pd.DataFrame(summary_data)

    # Create df_summary_present (last 2 months comparison)
    latest_col_idx = len(df_summary.columns) - 3
    prev_col_idx = len(df_summary.columns) - 6

    latest_col = df_summary.columns[latest_col_idx]
    previous_col = df_summary.columns[prev_col_idx]

    df_summary_present = df_summary[['Jenis Risiko', previous_col, latest_col]].copy()
    df_summary_present.columns = ['Kategori Risiko', 'previous_month', 'present_month']

    # Return latest column index for YTD
    latest_col_ytd_idx = months[-1]

    return {
        'df_ytd': df_ytd,
        'df_summary': df_summary,
        'df_summary_present': df_summary_present,
        'latest_col_idx': latest_col_idx,
        'latest_col_ytd_idx': latest_col_ytd_idx
    }
