@extends('layouts.app')

@section('content')
    <div class="container">
        
        @if (session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif
        @can('activity_log-create')
        <a href="{{ route('activity_log.create') }}" class="btn btn-primary mb-3">Create New</a>
        @endcan
        @if ($data->isEmpty())
            <div class="alert alert-warning">No data available.</div>
        @else
            <div class="card mb-4">
                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-bordered">
                            <thead class="thead-light">
                                <tr>
                                    <th>log_name</th><th>description</th><th>subject_type</th><th>event</th><th>subject_id</th><th>causer_type</th><th>causer_id</th><th>properties</th><th>batch_uuid</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                @foreach ($data as $item)
                                    <tr>
                                        <td>{{ $item->log_name }}</td><td>{{ $item->description }}</td><td>{{ $item->subject_type }}</td><td>{{ $item->event }}</td><td>{{ $item->subject_id }}</td><td>{{ $item->causer_type }}</td><td>{{ $item->causer_id }}</td><td>{{ $item->properties }}</td><td>{{ $item->batch_uuid }}</td>
                                        <td>
                                            @can('activity_log-edit')
                                            <a href="{{ route('activity_log.edit', $item->id) }}" class="btn btn-warning btn-sm">Edit</a>
                                            @endcan
                                            @can('activity_log-delete')
                                            <button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal" data-bs-target="#deleteModal{{ $item->id }}">Delete</button>
                                            @endcan
                                            <div class="modal fade" id="deleteModal{{ $item->id }}" tabindex="-1" aria-labelledby="deleteModalLabel{{ $item->id }}" aria-hidden="true">
                                                <div class="modal-dialog">
                                                    <div class="modal-content">
                                                        <div class="modal-header">
                                                            <h5 class="modal-title" id="deleteModalLabel{{ $item->id }}">Confirm Delete</h5>
                                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                                        </div>
                                                        <div class="modal-body">
                                                            Are you sure you want to delete this item?
                                                        </div>
                                                        <div class="modal-footer">
                                                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                                            <form action="{{ route('activity_log.destroy', $item->id) }}" method="POST" style="display:inline;">
                                                                @csrf
                                                                @method('DELETE')
                                                                <button type="submit" class="btn btn-danger">Delete</button>
                                                            </form>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
                <div class="card-footer">
                    {{ $data->links('pagination::bootstrap-5') }}
                </div>
            </div>
        @endif
    </div>
@endsection
