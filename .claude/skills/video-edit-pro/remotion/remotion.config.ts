// Transparent ProRes 4444 by default: the overlay is composited over the graded footage in FFmpeg.
import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("png");
Config.setPixelFormat("yuva444p10le");
Config.setCodec("prores");
Config.setProResProfile("4444");
