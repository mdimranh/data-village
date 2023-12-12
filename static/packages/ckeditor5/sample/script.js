ClassicEditor
	.create( document.querySelector( '#editor' ), {
			
	} )
	.then( editor => {
		window.editor = editor;
	} )
	.catch( handleSampleError );

function handleSampleError( error ) {
	const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

	const message = [
		'Oops, something went wrong!',
		`Please, report the following error on ${ issueUrl } with the build id "3z0ei8w89mdd-yh2w5gnneg9a" and the error stack trace:`
	].join( '\n' );

	console.error( message );
	console.error( error );
}
