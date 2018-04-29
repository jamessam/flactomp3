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

function makeFileList(path, extension) {
  let files = new Array();
  const rawList = fs.readdirSync(path);
  rawList.map(f => {
    const tempExtIndex = extension.length;
    let tempFExt = f.substring(f.length - tempExtIndex, f.length);
    // This needs to be extended to allow for capitalization variance
    if (tempFExt === extension) {
      files.push(f);
    }
  });
  return files
}

function validateFormat(format) {
  if (validFormats.indexOf(format) === -1) {
    throw new InvalidFormat(`${format} is not a valid format.`);
  }
  return;
}

// Synchronously validate if FFMPEG is added to the system

// Synchronously validate the paths passed from the cli and the format is valid
try {
  checkPath(hiResPath, 'high resolution path');
  checkPath(loResPath, 'low resolution path');
  validateFormat(format);
} catch (error) {
  console.log(error.error);
  process.exit();
}

// Synchronously make the file list
const fileList = makeFileList(hiResPath, format);

// A synchronolously map through the file list and create mp3s
// Make the FFMPEG command
// Excecute the command
