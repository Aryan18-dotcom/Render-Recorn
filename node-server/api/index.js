import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import fetch from "node-fetch";
import Razorpay from "razorpay";
import * as archiver from "archiver";
import dotenv from "dotenv";
dotenv.config();

const app = express();

// Resolve __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ENV config
const PYTHON_API_BASE = process.env.PYTHON_API_BASE;

// Razorpay keys
const RAZORPAY_KEY_ID = process.env.RAZORPAY_KEY_ID;
const RAZORPAY_KEY_SECRET = process.env.RAZORPAY_KEY_SECRET;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files from public/
// Replace the old __dirname paths with this in node-server/api/index.js:
const publicPath = path.join(process.cwd(), "public");

// Middleware
app.use(express.static(publicPath));

// Root route -> index.html
app.get("/", (req, res) => {
  res.sendFile(path.join(publicPath, "index.html"));
});

// API: generate specs (proxy to Python backend)
app.post("/api/generate", async (req, res) => {
  try {
    const { target_url } = req.body || {};
    if (!target_url) {
      return res.status(400).json({ error: "target_url is required" });
    }

    const response = await fetch(`${PYTHON_API_BASE}/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_url }),
    });

    if (!response.ok) {
      const text = await response.text();
      return res
        .status(response.status)
        .json({ error: "Python backend error", details: text });
    }

    const data = await response.json();

    return res.json({
      structure_md: data.structure_md,
      design_md: data.design_md,
      usecase_md: data.usecase_md,
    });
  } catch (err) {
    console.error("[Node API] /api/generate error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Razorpay: create order
app.post("/api/create-order", async (req, res) => {
  try {
    if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
      return res
        .status(500)
        .json({ error: "Razorpay is not configured on the server" });
    }

    const { amount, currency } = req.body || {};
    const finalAmount = amount || 100000; // Updated to match ₹1,000 parameter base unit
    const finalCurrency = currency || "INR";

    const instance = new Razorpay({
      key_id: RAZORPAY_KEY_ID,
      key_secret: RAZORPAY_KEY_SECRET,
    });

    const options = {
      amount: finalAmount,
      currency: finalCurrency,
      receipt: `receipt_${Date.now()}`,
    };

    const order = await instance.orders.create(options);

    return res.json({
      id: order.id,
      amount: order.amount,
      currency: order.currency,
      keyId: RAZORPAY_KEY_ID,
    });
  } catch (err) {
    console.error("[Node API] /api/create-order error:", err);
    res.status(500).json({ error: "Failed to create Razorpay order" });
  }
});

// Generate ZIP from markdowns
app.post("/api/generate-zip", async (req, res) => {
  try {
    const { structure_md, design_md, usecase_md } = req.body || {};

    if (!structure_md || !design_md || !usecase_md) {
      return res.status(400).json({
        error: "ZIP_INPUT_ERROR",
        message: "All three markdown contents are required to generate ZIP.",
      });
    }

    res.setHeader("Content-Type", "application/zip");
    res.setHeader(
      "Content-Disposition",
      'attachment; filename="webagent_specs_bundle.zip"'
    );

    const archive = archiver("zip", { zlib: { level: 9 } });

    archive.on("error", (err) => {
      console.error("[Node API] /api/generate-zip archiver error:", err);
      res.status(500).end();
    });

    archive.pipe(res);
    archive.append(structure_md, { name: "structure.md" });
    archive.append(design_md, { name: "design.md" });
    archive.append(usecase_md, { name: "usecase.md" });
    archive.finalize();

  } catch (err) {
    console.error("[Node API] /api/generate-zip unexpected error:", err);
    if (!res.headersSent) {
      res.status(500).json({
        error: "ZIP_INTERNAL_ERROR",
        message: "Failed to generate ZIP file.",
      });
    }
  }
});

if (process.env.VERCEL !== "1") {
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log(`Express server running on http://localhost:${port}`);
  });
}