ClassicEditor
	.create( document.querySelector( '#editor' ), {
			
	} )
	.then( editor => {
		window.editor = editor;
	} )
	.catch( handleSampleError );

	editor.ui.componentFactory.add('customButton', locale => {
		const view = new editor.ButtonView(locale);
		view.set({
			label: 'Custom Button',
			icon: 'https://csod072009s.searchunify.com/resources/Assets/upload-image.svg',
			tooltip: true
		});
		view.on('execute', () => {
			editor.execute('customCommand');
		});

		return view;
	});

function handleSampleError( error ) {
	const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

	const message = [
		'Oops, something went wrong!',
		`Please, report the following error on ${ issueUrl } with the build id "3z0ei8w89mdd-yh2w5gnneg9a" and the error stack trace:`
	].join( '\n' );

	console.error( message );
	console.error( error );
}
