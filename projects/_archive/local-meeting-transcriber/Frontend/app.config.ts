import { ConfigContext, ExpoConfig } from "expo/config";
export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: "LMT",
  slug: "local-meeting-transcriber",
  extra: {
    // Empty string means same-origin /api routes in Vercel web builds.
    API_BASE: process.env.API_BASE || "",
  },
  ios: { 
    supportsTablet: true,
    bundleIdentifier: "com.lmt.app"
  },
  android: { 
    package: "com.lmt.app",
    adaptiveIcon: {
      foregroundImage: "./assets/adaptive-icon.png",
      backgroundColor: "#ffffff"
    }
  }
});
