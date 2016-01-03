v1.3.0 - 2016-01-03
===================

- Require Python 3.5 for new asyncio async/await syntax.
  - Update code to use async/await.
  - LoopTestCase now requires async test methods to be declared as such.
- Add clear() and len() support to Collection.
- Add overridable Script.handle_keyboard_interrupt handler.
- Use relative imports in library code.

v1.2.0 - 2015-08-04
===================

- Added modules:
  - toolrack.async
  - toolrack.property
  - toolrack.testing.async

- Moved TempDirFixture to the toolrack.testing.fixtures module.
- Added password-generator script.


v1.1.0 - 2015-06-25
===================

- Add toolrack.threading module.


v1.0.1 - 2015-06-19
===================

- Add TempDirFixture.join.


v1.0.0 - 2015-05-30
===================

- Finalize switch to python3.
- Code cleanups.


v0.3.0 - 2015-05-22
===================

- Switch to python3.


v0.2.0 - 2015-04-22
===================

- Add description to ConfigKeys.
- Config.keys() now return a list of sorted ConfigKeys.
- Fix issue with flatten_dict() when the key is not a string.
- Add Collecion.sorted().


v0.1.0 - 2015-04-08
===================

- Added toolrack.config module.
- Fixed use of mkstemp in TempDirFixture.
  

v0.0.3 - 2015-03-25
===================

- Added modules:
  - toolrack.collect
  - toolrack.convert
  - toolrack.iterate


v0.0.2 - 2015-03-25
===================

- Fix setup.py.


v0.0.1 - 2015-03-24
===================

- First release.
