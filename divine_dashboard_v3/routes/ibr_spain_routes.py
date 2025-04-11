from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
import os
import json
from datetime import datetime

from divine_dashboard_v3.components.ibr_spain.micro_modules.events_manager import EventsManager

# Create Blueprint
ibr_spain_bp = Blueprint('ibr_spain', __name__, url_prefix='/ibr-spain')

# Initialize the events manager
events_manager = EventsManager()

@ibr_spain_bp.route('/')
def index():
    """Render the main IBR España dashboard."""
    # Get upcoming events for display
    upcoming_events = events_manager.get_upcoming_events(days=30)
    
    return render_template('ibr_spain/index.html', 
                          upcoming_events=upcoming_events)

@ibr_spain_bp.route('/events')
def events_page():
    """Render the events page."""
    # Get view type from query parameters (default to list)
    view_type = request.args.get('view', 'list')
    
    # Get event type filter if provided
    event_type = request.args.get('type')
    
    # Get date range if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Get events based on filters
    if event_type:
        events = events_manager.get_events_by_type(event_type)
    elif start_date and end_date:
        events = events_manager.get_events_by_date_range(start_date, end_date)
    else:
        # Default to all events
        events = events_manager.get_all_events()
    
    return render_template('ibr_spain/events.html', 
                          events=events,
                          view_type=view_type,
                          event_type=event_type,
                          start_date=start_date,
                          end_date=end_date)

@ibr_spain_bp.route('/events/create', methods=['GET', 'POST'])
def create_event():
    """Handle event creation."""
    if request.method == 'POST':
        # Get form data
        event_data = {
            'title': request.form.get('title'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'end_time': request.form.get('end_time'),
            'location': request.form.get('location'),
            'description': request.form.get('description'),
            'type': request.form.get('type'),
            'recurring': request.form.get('recurring') == 'on',
            'recurrence_pattern': request.form.get('recurrence_pattern')
        }
        
        # Add the event
        new_event = events_manager.add_event(event_data)
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('ibr_spain.events_page'))
    
    # For GET request, render the creation form
    return render_template('ibr_spain/event_form.html', 
                          event=None,
                          action='create')

@ibr_spain_bp.route('/events/<event_id>')
def view_event(event_id):
    """View a single event."""
    event = events_manager.get_event(event_id)
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('ibr_spain.events_page'))
    
    return render_template('ibr_spain/event_detail.html', event=event)

@ibr_spain_bp.route('/events/<event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    """Handle event editing."""
    event = events_manager.get_event(event_id)
    
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('ibr_spain.events_page'))
    
    if request.method == 'POST':
        # Get form data
        update_data = {
            'title': request.form.get('title'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'end_time': request.form.get('end_time'),
            'location': request.form.get('location'),
            'description': request.form.get('description'),
            'type': request.form.get('type'),
            'recurring': request.form.get('recurring') == 'on',
            'recurrence_pattern': request.form.get('recurrence_pattern')
        }
        
        # Update the event
        updated_event = events_manager.update_event(event_id, update_data)
        
        if updated_event:
            flash('Event updated successfully!', 'success')
        else:
            flash('Failed to update event', 'error')
            
        return redirect(url_for('ibr_spain.view_event', event_id=event_id))
    
    # For GET request, render the edit form
    return render_template('ibr_spain/event_form.html', 
                          event=event,
                          action='edit')

@ibr_spain_bp.route('/events/<event_id>/delete', methods=['POST'])
def delete_event(event_id):
    """Handle event deletion."""
    success = events_manager.delete_event(event_id)
    
    if success:
        flash('Event deleted successfully!', 'success')
    else:
        flash('Failed to delete event', 'error')
        
    return redirect(url_for('ibr_spain.events_page'))

# API routes for AJAX calls
@ibr_spain_bp.route('/api/events', methods=['GET'])
def api_get_events():
    """API endpoint to get events."""
    # Get filter parameters
    event_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Get events based on filters
    if event_type:
        events = events_manager.get_events_by_type(event_type)
    elif start_date and end_date:
        events = events_manager.get_events_by_date_range(start_date, end_date)
    else:
        # Default to upcoming events
        events = events_manager.get_upcoming_events()
    
    return jsonify(events)

@ibr_spain_bp.route('/api/events/<event_id>', methods=['GET'])
def api_get_event(event_id):
    """API endpoint to get a single event."""
    event = events_manager.get_event(event_id)
    
    if not event:
        return jsonify({"error": "Event not found"}), 404
    
    return jsonify(event)

@ibr_spain_bp.route('/api/events', methods=['POST'])
def api_create_event():
    """API endpoint to create an event."""
    try:
        # Get JSON data
        event_data = request.get_json()
        
        # Add the event
        new_event = events_manager.add_event(event_data)
        
        return jsonify(new_event), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ibr_spain_bp.route('/api/events/<event_id>', methods=['PUT'])
def api_update_event(event_id):
    """API endpoint to update an event."""
    try:
        # Get JSON data
        update_data = request.get_json()
        
        # Update the event
        updated_event = events_manager.update_event(event_id, update_data)
        
        if not updated_event:
            return jsonify({"error": "Event not found"}), 404
        
        return jsonify(updated_event)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@ibr_spain_bp.route('/api/events/<event_id>', methods=['DELETE'])
def api_delete_event(event_id):
    """API endpoint to delete an event."""
    success = events_manager.delete_event(event_id)
    
    if not success:
        return jsonify({"error": "Event not found"}), 404
    
    return jsonify({"message": "Event deleted successfully"})

# Utility routes
@ibr_spain_bp.route('/generate-sample-events', methods=['POST'])
def generate_sample_events():
    """Generate sample events for testing."""
    count = int(request.form.get('count', 5))
    events_manager.generate_sample_events(count)
    
    flash(f'{count} sample events generated!', 'success')
    return redirect(url_for('ibr_spain.events_page')) 