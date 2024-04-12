contract Test {
  function a() {
   a();
// ^ defined: 2
  }

  function b() {
    a();
//  ^ defined: 2
  }

  function c() {

  }
}
