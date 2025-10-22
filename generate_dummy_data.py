import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Create dummy data from August-2024 to August-2025
def generate_dummy_data():
    np.random.seed(42)  # For reproducibility

    # Create parameter list (146 rows total)
    parameters = ['Parameter', 'Aset Investasi', 'Deposito Berjangka', 'Obligasi Korporasi',
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
                  'Indak Lanjut Pengaduan', 'Jumlah Pemberitaan Negatif', 'Jumlah Pemberitaan Negatif Dalam 1 Tahun']

    # Generate months from August 2024 to August 2025
    start_date = datetime(2024, 8, 1)
    months_data = []
    for i in range(13):  # 13 months (Aug 2024 to Aug 2025)
        date = start_date + relativedelta(months=i)
        months_data.append({
            'month_name': date.strftime('%B'),
            'year': date.year,
            'short_name': date.strftime('%b')
        })

    # Create Data_YTD sheet
    ytd_columns = ['Unnamed: 0', 'Unnamed: 1']

    # Add columns for each month (year column + month column)
    for month_info in months_data:
        ytd_columns.append(month_info['month_name'])
        ytd_columns.append(f"Unnamed: {len(ytd_columns)}")

    # Initialize data dictionary
    ytd_data = {}

    # Add row numbers
    ytd_data['Unnamed: 0'] = ['No'] + list(range(1, len(parameters)))

    # Add parameters
    ytd_data['Unnamed: 1'] = parameters

    # Generate data for each month
    col_idx = 2
    for month_info in months_data:
        month_name = month_info['month_name']
        year = month_info['year']

        # Year column
        year_col = [year] + [np.nan] * (len(parameters) - 1)
        ytd_data[month_name] = year_col

        # Data column
        data_values = [month_name]  # First row is month name

        # Generate realistic financial data
        for i in range(1, len(parameters)):
            if i <= 10:  # Asset related (in billions)
                data_values.append(round(np.random.uniform(500, 5000), 2))
            elif i <= 16:  # Liabilities and Equity
                data_values.append(round(np.random.uniform(300, 3000), 2))
            elif i <= 25:  # Premium related
                data_values.append(round(np.random.uniform(100, 1000), 2))
            elif i <= 44:  # Various income/expenses
                data_values.append(round(np.random.uniform(50, 800), 2))
            elif i == 52:  # RBC - specific index
                data_values.append(round(np.random.uniform(120, 250), 2))
            elif i <= 100:  # Various ratios
                data_values.append(round(np.random.uniform(0.1, 5), 2))
            elif i <= 116:  # Count data
                data_values.append(int(np.random.uniform(10, 1000)))
            elif i <= 120:  # Fraud and complaints
                data_values.append(int(np.random.uniform(0, 50)))
            elif i <= 130:  # Percentages
                data_values.append(round(np.random.uniform(1, 100), 2))
            else:  # Other counts
                data_values.append(int(np.random.uniform(0, 20)))

        ytd_data[f'Unnamed: {col_idx + 1}'] = data_values
        col_idx += 2

    df_ytd = pd.DataFrame(ytd_data)

    # Create Summary sheet
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
        '',  # Empty row
        'Composite Score',
    ]

    summary_data = {}
    summary_data['Unnamed: 0'] = [''] * len(risk_categories)
    summary_data['Jenis Risiko'] = risk_categories

    # Generate summary data for each month
    for month_info in months_data:
        month_name = month_info['month_name']
        year = month_info['year']

        # Generate risk scores
        scores = []
        for cat in risk_categories:
            if cat == '':
                scores.append('-')
            elif cat == 'Composite Score':
                # Composite score is average of all risk scores
                avg_score = np.mean([s for s in scores[:-1] if s != '-'])
                scores.append(round(avg_score, 2))
            else:
                scores.append(round(np.random.uniform(1.5, 4.5), 2))

        # Add three columns per month: score, weighted, classification
        summary_data[f'{month_name}-{year}'] = [year] * len(risk_categories)
        summary_data[f'{month_name}-score'] = scores
        summary_data[f'{month_name}-weighted'] = [s if s == '-' else round(s * 0.8, 2) for s in scores]
        summary_data[f'{month_name}-classification'] = [
            '-' if s == '-' else ('High' if s > 3.5 else 'Moderate' if s > 2.5 else 'Low')
            for s in scores
        ]

    df_summary = pd.DataFrame(summary_data)

    # Create Excel file
    with pd.ExcelWriter('dummy_data_2024_2025.xlsx', engine='openpyxl') as writer:
        df_ytd.to_excel(writer, sheet_name='Data_YTD', index=False)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)

    print("✅ Dummy data file 'dummy_data_2024_2025.xlsx' has been created successfully!")
    print("📅 This file contains data from August-2024 to August-2025 (13 months)")
    print(f"📊 Data_YTD sheet: {len(df_ytd)} rows, {len(df_ytd.columns)} columns")
    print(f"📊 Summary sheet: {len(df_summary)} rows, {len(df_summary.columns)} columns")

if __name__ == "__main__":
    generate_dummy_data()
