"""Module for generating sync status reports."""
from datetime import datetime
from textwrap import dedent
from flask import jsonify

def generate_sync_report(mapping_list, actual_count, ynab_count, errors):
    """Generate a detailed sync report."""
    # Derive stats from mapping data
    actual_accounts = sum(1 for m in mapping_list.values() 
                        if m.get('actual_account_id') and not m.get('actual_do_not_map'))
    ynab_accounts = sum(1 for m in mapping_list.values() 
                       if m.get('ynab_account_id') and not m.get('ynab_do_not_map'))
    
    # Get last sync times
    actual_last_sync = max((m.get('actual_synced_datetime', '2024-01-01T00:00:00Z') 
                           for m in mapping_list.values() if m.get('actual_account_id')), 
                           default='Never')
    ynab_last_sync = max((m.get('ynab_synced_datetime', '2024-01-01T00:00:00Z') 
                         for m in mapping_list.values() if m.get('ynab_account_id')), 
                         default='Never')

    # Generate summary text
    errors_multiline = "\n".join(errors) if errors else "No errors"



    summary = dedent(f"""Sync completed at {datetime.now().isoformat()}

        Actual Budget:
        - Accounts configured: {actual_accounts}
        - New transactions created: {actual_count}
        - Previous sync time: {actual_last_sync}

        YNAB:
        - Accounts configured: {ynab_accounts}
        - New transactions created: {ynab_count}
        - Previous sync time: {ynab_last_sync}

        "Errors encountered: {errors_multiline}""")

    # Generate response
    if errors:
        return jsonify({
            "status": "partial_failure",
            "stats": {
                "actual": {
                    "accounts": actual_accounts,
                    "transactions_created": actual_count,
                    "last_sync": actual_last_sync
                },
                "ynab": {
                    "accounts": ynab_accounts,
                    "transactions_created": ynab_count,
                    "last_sync": ynab_last_sync
                }
            },
            "errors": errors,
            "summary": summary
        }), 500
    else:
        return jsonify({
            "status": "success",
            "stats": {
                "actual": {
                    "accounts": actual_accounts,
                    "transactions_created": actual_count,
                    "last_sync": actual_last_sync
                },
                "ynab": {
                    "accounts": ynab_accounts,
                    "transactions_created": ynab_count,
                    "last_sync": ynab_last_sync
                }
            },
            "summary": summary
        }), 200