const socket = io.connect();

document.getElementById('startButton').addEventListener('click', () => {
    const amplificationFactor = document.getElementById('amplification').value;
    const noiseReductionLevel = document.getElementById('noiseReduction').value;

    socket.emit('start_audio', {
        amplificationFactor: parseFloat(amplificationFactor),
        noiseReductionLevel: parseFloat(noiseReductionLevel)
    });
});

document.getElementById('stopButton').addEventListener('click', () => {
    socket.emit('stop_audio');
});

document.getElementById('amplification').addEventListener('input', (event) => {
    document.getElementById('amplificationValue').innerText = event.target.value;
});

document.getElementById('noiseReduction').addEventListener('input', (event) => {
    document.getElementById('noiseReductionValue').innerText = event.target.value + '%';
});
