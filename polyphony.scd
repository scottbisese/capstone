// initialize a midi client
MIDIClient.init;
// Connect all ins and outs midi-wise
MIDIIn.connectAll; // Optionally connect all MIDI sources
// boot the audio server, known as JACK
s.boot;

// make a note array, to help with note on and off
~notes = Array.newClear(128);

// make a synth
(
SynthDef.new(\tone,{
	arg freq=440, amp=0.3, gate=0;
	var sig,env;
	sig = SinOsc.ar(freq)!2;
	env = EnvGen.kr(Env.adsr, gate, doneAction:2);
	sig = sig * env * amp;
	Out.ar(0, sig);
}).add;


// set note one actions
MIDIdef.noteOn(\noteOnTest, {
	arg vel, nn, chan, src;
	[vel,nn,chan,src].postln;
	~notes[nn] = Synth.new(
		\tone,
		[
			\freq, nn.midicps,
			\amp, vel.linexp(1,127,0.01,0.3),
			\gate, 1,
		]
	);
});

// add in note off actions as well, so notes dont just play forever
MIDIdef.noteOff(\noteOffTest, {
	arg vel, nn;
	[vel, nn].postln;
	~notes[nn].set(\gate, 0);
	~notes[nn] = nil;
});
)
/*x = Synth.new(\tone, [\gate, 1]);
x.set(\gate, 0);*/

// test audio here.
// { SinOsc.ar(440, 0, 0.2) }.play;
