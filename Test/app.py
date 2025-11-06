from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import ElectionDB

app = Flask(__name__)
db = ElectionDB()

@app.route('/')
def index():
    """Home page with overview"""
    units = db.get_all_polling_units()
    lgas = db.get_all_lgas()
    
    # Get recent results for display
    recent_results = []
    for unit in units[:5]:  # Show first 5 units
        results = db.get_results_by_polling_unit(unit.id)
        if results:
            total_votes = sum(r.votes for r in results)
            recent_results.append({
                'unit': unit,
                'total_votes': total_votes,
                'parties': len(results)
            })
    
    return render_template('index.html', 
                         recent_results=recent_results,
                         total_units=len(units),
                         total_lgas=len(lgas))

@app.route('/polling-unit')
def polling_unit():
    """Individual polling unit results"""
    unit_id = request.args.get('unit_id', type=int)
    units = db.get_all_polling_units()
    
    if unit_id:
        unit = db.get_polling_unit_by_id(unit_id)
        results = db.get_results_by_polling_unit(unit_id)
        return render_template('polling_unit.html', 
                             units=units, 
                             selected_unit=unit,
                             results=results)
    
    return render_template('polling_unit.html', units=units)

@app.route('/lga-summary')
def lga_summary():
    """LGA summary results"""
    lga_name = request.args.get('lga')
    lgas = db.get_all_lgas()
    
    if lga_name:
        party_totals = db.get_party_totals_by_lga(lga_name)
        total_votes = sum(party_totals.values())
        leading_party = max(party_totals.items(), key=lambda x: x[1]) if party_totals else (None, 0)
        
        return render_template('lga_summary.html',
                             lgas=lgas,
                             selected_lga=lga_name,
                             party_totals=party_totals,
                             total_votes=total_votes,
                             leading_party=leading_party)
    
    return render_template('lga_summary.html', lgas=lgas)

@app.route('/new-result', methods=['GET', 'POST'])
def new_result():
    """Add new polling unit results"""
    units = db.get_all_polling_units()
    
    if request.method == 'POST':
        unit_id = request.form.get('unit_id', type=int)
        party_name = request.form.get('party_name', '').strip().upper()
        votes = request.form.get('votes', type=int)
        
        if unit_id and party_name and votes is not None:
            db.add_new_result(unit_id, party_name, votes)
            return redirect(url_for('polling_unit', unit_id=unit_id))
    
    return render_template('new_result.html', units=units)

@app.route('/all-units')
def all_units():
    """View all polling units"""
    units = db.get_all_polling_units()
    
    # Calculate totals for each unit
    units_with_totals = []
    for unit in units:
        results = db.get_results_by_polling_unit(unit.id)
        total_votes = sum(r.votes for r in results)
        units_with_totals.append({
            'unit': unit,
            'total_votes': total_votes,
            'party_count': len(results)
        })
    
    return render_template('all_units.html', units=units_with_totals)

# API endpoints for potential frontend enhancements
@app.route('/api/polling-units')
def api_polling_units():
    units = db.get_all_polling_units()
    return jsonify([{'id': u.id, 'name': u.name, 'lga': u.lga} for u in units])

@app.route('/api/results/<int:unit_id>')
def api_unit_results(unit_id):
    results = db.get_results_by_polling_unit(unit_id)
    return jsonify([{'party': r.party_name, 'votes': r.votes} for r in results])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)