contract Test {
  uint st;
  function a() {
   a();
// ^ defined: 3
  }

  function b() {
    a();
//  ^ defined: 3
  }

  function c() {
    st = 1;
  // ^ defined: 2
  }
}
