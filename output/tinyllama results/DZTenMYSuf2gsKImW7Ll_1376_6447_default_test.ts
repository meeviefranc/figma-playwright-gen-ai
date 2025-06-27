```
// Test for Default: Follow me on:, Chiip, Aspen Lubin
// Generate Playwright TypeScript test. Check visibility.

import { FollowMeOn } from "../src/FollowMeOn";

describe("Default: Follow me on:", () => {
  it("should display the text 'Follow me on:'", async () => {
    const followMeOn = new FollowMeOn();
    await followMeOn.run();
    expect(await followMeOn.getOutput()).toContain("Follow me on:");
  });
});
```