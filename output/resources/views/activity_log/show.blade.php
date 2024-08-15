@extends('layouts.app')

@section('content')
    <div class="container">
        
        @if (session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif
        <div class="card mb-4">
            <div class="card-body">
                <p><strong>Log_name:</strong> {{ $data->log_name }}</p><p><strong>Description:</strong> {{ $data->description }}</p><p><strong>Subject_type:</strong> {{ $data->subject_type }}</p><p><strong>Event:</strong> {{ $data->event }}</p><p><strong>Subject_id:</strong> {{ $data->subject_id }}</p><p><strong>Causer_type:</strong> {{ $data->causer_type }}</p><p><strong>Causer_id:</strong> {{ $data->causer_id }}</p><p><strong>Properties:</strong> {{ $data->properties }}</p><p><strong>Batch_uuid:</strong> {{ $data->batch_uuid }}</p>
            </div>
        </div>
        <a href="{{ route('activity_log.edit', $data->id) }}" class="btn btn-warning">Edit</a>
        <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal{{ $data->id }}">Delete</button>
        <div class="modal fade" id="deleteModal{{ $data->id }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ $data->id }}" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="deleteModalLabel{{ $data->id }}">Confirm Delete</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to delete this item?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <form action="{{ route('activity_log.destroy', $data->id) }}" method="POST" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger">Delete</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection
