const fs = require('fs');

const hiResPath = process.argv[2];
const loResPath = process.argv[3];
const format = process.argv[4];

const validFormats = ['flac', 'wav'];

function InvalidFormat(error) {
  this.error = error;
  this.name = 'InvalidFormat';
}

function PathNotFoundError(error) {
  this.error = error;
  this.name = 'PathNotFoundError';
}

function checkPath(path, value) {
  if (!fs.existsSync(path)) {
    throw new PathNotFoundError(
      `That value for the ${value} is invalid. Please try running the script again.`
    );
  }
  return;
}

function validateFormat(format) {
  if (validFormats.indexOf(format) === -1) {
    throw new InvalidFormat(`${format} is not a valid format.`);
  }
  return;
}

// Validate if FFMPEG is added to the system

// Validate the paths passed from the cli and the format is valid
try {
  checkPath(hiResPath, 'high resolution path');
  checkPath(loResPath, 'low resolution path');
  validateFormat(format);
} catch (error) {
  console.log(error.error);
  process.exit();
}

// Make the file list

// Cycle the file list and create mp3s
  // Make the FFMPEG command
  // Excecute the command
